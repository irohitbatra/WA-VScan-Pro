import os, html, json
from datetime import datetime

def generate_report(target, findings, duration, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    severities = ["Critical","High","Medium","Low","Info"]
    counts = {s:0 for s in severities}

    rows = []
    for f in findings or []:
        sev = f.get("severity", "Info")
        if sev not in counts:
            sev = "Info"
        counts[sev] += 1

        rows.append(
            f"""
            <tr>
                <td>{html.escape(str(f.get('id','')))}</td>
                <td>{html.escape(str(f.get('name','')))}</td>
                <td><span class="sev {sev.lower()}">{sev}</span></td>
                <td>{html.escape(str(f.get('finding','')))}</td>
                <td><div class="detail-box"><pre>{html.escape(str(f.get('details','')))}</pre></div></td>
            </tr>
            """
        )

    rows_html = "\n".join(rows) if rows else "<tr><td colspan='5'>No findings.</td></tr>"
    data_array = json.dumps([counts[s] for s in severities])
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html_out = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>WA-VScan Pro – Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {{
  background:#061020;
  color:#d7e9ff;
  font-family:Inter, Arial;
  margin:20px;
}}
.card {{
  background:#0b1430;
  padding:18px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,0.06);
  margin-bottom:16px;
}}
header {{
  display:flex;
  align-items:center;
  justify-content:space-between;
}}
.logo {{
  background:#002a44;
  width:58px;
  height:58px;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:10px;
  color:#00ffcc;
  font-weight:bold;
}}
table {{
  width:100%;
  border-collapse:collapse;
  table-layout:fixed;
}}
td,th {{
  padding:10px;
  border-bottom:1px solid rgba(255,255,255,0.06);
  font-size:13px;
  word-break:break-word;
}}
.detail-box {{
  max-height:150px;
  overflow:auto;
  background:rgba(255,255,255,0.05);
  border-radius:8px;
  padding:6px;
}}
.sev {{
  padding:5px 7px;
  border-radius:6px;
  font-weight:bold;
  color:#000;
}}
.sev.critical {{ background:#ff4d4d; }}
.sev.high     {{ background:#ff884d; }}
.sev.medium   {{ background:#ffd24d; }}
.sev.low      {{ background:#79e69b; }}
.sev.info     {{ background:#6bb3ff; }}

.chart-box {{
  width:180px;
  height:180px;
  margin:auto;
}}

.footer {{
  text-align:right;
  font-size:12px;
  margin-top:20px;
  color:#9bb0d1;
}}
</style>
</head>

<body>

<div class="card">
<header>
  <div class="logo">WA</div>
  <div>
    <h2 style="margin:0">WA-VScan Pro Report</h2>
    <div style="font-size:13px;color:#9bb0d1">
      Target: <b>{html.escape(target)}</b><br>
      Generated: {ts}<br>
      Duration: {duration:.2f}s
    </div>
  </div>
</header>
</div>

<div class="card">
  <h3>Severity Distribution</h3>
  <div class="chart-box"><canvas id="chart"></canvas></div>
</div>

<div class="card">
  <h3>Findings</h3>
  <table>
    <thead>
      <tr><th>ID</th><th>Name</th><th>Severity</th><th>Finding</th><th>Details</th></tr>
    </thead>
    <tbody>
    {rows_html}
    </tbody>
  </table>
</div>

<div class="footer">
  Made with <span style="color:#ff6b6b">❤</span> by Rohit Batra
</div>

<script>
const ctx = document.getElementById("chart").getContext("2d");

const chartData = {{
    labels: ["Critical","High","Medium","Low","Info"],
    datasets: [{{
        data: {data_array},
        backgroundColor: ["#ff4d4d","#ff884d","#ffd24d","#79e69b","#6bb3ff"]
    }}]
}};

new Chart(ctx, {{
    type: "doughnut",
    data: chartData,
    options: {{
        cutout: "55%",
        plugins: {{ legend: {{ display:false }} }}
    }}
}});
</script>

</body>
</html>
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    return out_path
