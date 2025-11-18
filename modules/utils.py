from urllib.parse import urlparse, urlunparse
def normalize_url(u):
    if not u:
        raise ValueError("Empty URL")
    u = u.strip()
    if not u.startswith("http"):
        u = "http://" + u
    parsed = urlparse(u)
    path = parsed.path or '/'
    new = parsed._replace(path=path)
    return urlunparse(new).rstrip('/')
