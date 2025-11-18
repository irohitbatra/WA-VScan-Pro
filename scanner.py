#!/usr/bin/env python3
import time, json, csv, os
from modules.checks import run_all_checks
from modules.report_v2 import generate_report
from modules.utils import normalize_url
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scan_target(target, threads=6, timeout=8):
    target = normalize_url(target)
    start = time.time()
    results = run_all_checks(target, threads=threads, timeout=timeout)
    duration = time.time() - start
    os.makedirs("results", exist_ok=True)
    json_path = os.path.join("results", "results.json")
    with open(json_path, "w") as f:
        json.dump({"target": target, "duration": duration, "checks": results}, f, indent=2)
    csv_path = os.path.join("results", "results.csv")
    with open(csv_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id","name","severity","finding","details"])
        for c in results:
            writer.writerow([c.get("id"), c.get("name"), c.get("severity"), c.get("finding"), c.get("details")])
    report_path = os.path.join("results", "report_v2.html")
    generate_report(target, results, duration, report_path)
    return {"json": json_path, "csv": csv_path, "html": report_path}

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python3 scanner.py <target>')
        sys.exit(1)
    target = sys.argv[1]
    print('Starting scan:', target)
    out = scan_target(target)
    print('Report:', out)
