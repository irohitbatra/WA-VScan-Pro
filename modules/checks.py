import requests, threading, time, random
from urllib.parse import urljoin
requests.packages.urllib3.disable_warnings()
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/121.0 Safari/537.36"
]
DEFAULT_HEADERS = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9"}
def http_get(url, params=None, timeout=8, max_retries=3):
    for attempt in range(1, max_retries+1):
        headers = dict(DEFAULT_HEADERS)
        headers["User-Agent"] = random.choice(USER_AGENTS)
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=timeout, verify=False)
            return resp, None
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.ChunkedEncodingError) as e:
            time.sleep(0.5 * (2 ** (attempt-1)))
            last = e
            continue
        except Exception as e:
            return None, str(e)
    return None, str(last)
def make_result(id, name, severity, finding, details):
    return {"id": id, "name": name, "severity": severity, "finding": finding, "details": details}
def check_security_headers(target):
    r, err = http_get(target)
    if err:
        return make_result("HDR01","Security Headers","Info","Error", str(err))
    required = ["X-Frame-Options","X-XSS-Protection","Strict-Transport-Security","Content-Security-Policy","X-Content-Type-Options"]
    missing = [h for h in required if h not in r.headers]
    if missing:
        return make_result("HDR01","Missing Security Headers","Medium", f"{len(missing)} headers missing", ", ".join(missing))
    return None
def check_directory_listing(target):
    r, err = http_get(target)
    if not r:
        return None
    txt = r.text or ""
    if "Index of /" in txt or "<title>Index of" in txt:
        return make_result("DIR01","Directory Listing","High","Directory listing detected","Index listing")
    return None
def check_backup_files(target):
    candidates = ["backup.zip","db.sql","site.bak","config.old","admin.bak",".env","config.php~","backup.tar.gz"]
    for p in candidates:
        url = urljoin(target.rstrip('/')+'/', p)
        r, err = http_get(url, timeout=6)
        if r and r.status_code==200 and len(r.content)>50:
            return make_result("BKP01","Exposed Backup File","Critical", f"Backup found: {p}", url)
    return None
def check_sql_errors(target):
    payload = "' OR '1'='1"
    r, err = http_get(target, params={"id":payload}, timeout=6)
    if not r:
        return None
    txt = (r.text or "").lower()
    if any(e in txt for e in ["mysql","syntax error","sqlstate","pdoexception","warning: mysql","ora-"]):
        return make_result("SQL01","SQL Error Disclosure","High","SQL error strings found","Payload used: "+payload)
    return None
def check_xss_reflected(target):
    payload = "<script>alert(1)</script>"
    params = ['q','search','s','query','id','name']
    for p in params:
        r, err = http_get(target, params={p:payload}, timeout=6)
        if not r:
            continue
        if payload in (r.text or ""):
            return make_result("XSS01","Reflected XSS","High", f"Payload reflected in param {p}", r.url)
    return None
def check_robots(target):
    r, err = http_get(urljoin(target.rstrip('/')+'/', 'robots.txt'), timeout=5)
    if r and r.status_code==200 and ("Disallow" in (r.text or "") or "/admin" in (r.text or "")):
        return make_result("ROB01","Robots.txt Sensitive Paths","Low","robots.txt contains disallow entries", r.text[:800])
    return None
def check_server_banner(target):
    r, err = http_get(target, timeout=6)
    if not r:
        return None
    srv = r.headers.get('Server','')
    return make_result("BAN01","Server Banner","Info", f"Server header: {srv}", str(dict(r.headers)))
def run_all_checks(target, threads=6, timeout=8):
    checks = [check_security_headers, check_directory_listing, check_backup_files, check_sql_errors, check_xss_reflected, check_robots, check_server_banner]
    results = []
    threads_list = []
    def run_check(fn):
        try:
            r = fn(target)
            if r:
                results.append(r)
        except Exception as e:
            results.append(make_result('ERR','Check Exception','Info','Exception in check', str(e)))
    for chk in checks:
        t = threading.Thread(target=run_check, args=(chk,))
        t.start()
        threads_list.append(t)
    for t in threads_list:
        t.join()
    return results
