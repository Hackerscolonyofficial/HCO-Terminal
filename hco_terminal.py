#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCO Terminal — Neon Portal (single-file)
Author: Azhar | Hackers Colony
Run (Termux):
  pkg update -y
  pkg install python -y
  pip install flask
  python3 hco_terminal.py
"""

from flask import Flask, render_template_string
import threading, subprocess, shutil, time, webbrowser, os, sys

# ---------- Config (edit your links) ----------
APP_NAME = "HCO Terminal"
HOST = "127.0.0.1"
PORT = 8080

TELEGRAM_LINK = "https://t.me/HackersColony"
WHATSAPP_LINK = "https://chat.whatsapp.com/BHwZHVntVicI8zdmfbJoQV"
YOUTUBE_LINK  = "https://youtube.com/@hackers_colony_tech?si=51CiCi_q1_CwiTnc"
WEBSITE_LINK  = "https://hackerscolonyofficial.blogspot.com/?m=1"
LEARN_LINK    = "https://tryhackme.com"   # example learning link

# ---------- Flask app ----------
app = Flask(__name__)

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{APP_NAME} — Hackers Colony Portal</title>
<link rel="icon" href="data:,">
<style>
  /* Reset */
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{height:100%}}
  body {{
    font-family: Inter, "Segoe UI", Roboto, system-ui, -apple-system, sans-serif;
    background: radial-gradient(1200px 600px at 10% 10%, #07102a 0%, #02020a 35%, #000 100%);
    color:#e6eef6;
    -webkit-font-smoothing:antialiased;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:24px;
  }}

  .panel {{
    width:100%;
    max-width:980px;
    border-radius:16px;
    padding:28px;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    box-shadow: 0 10px 40px rgba(2,6,23,0.7), inset 0 1px 0 rgba(255,255,255,0.02);
    backdrop-filter: blur(6px);
  }}

  .top {{
    display:flex;
    align-items:center;
    gap:18px;
  }}
  .badge {{
    width:72px;height:72px;border-radius:14px;
    display:flex;align-items:center;justify-content:center;
    background: linear-gradient(135deg,#09182b,#05283a);
    box-shadow: 0 6px 20px rgba(0,170,150,0.08);
    position:relative;
    overflow:hidden;
  }}
  .badge:after{{
    content:"";
    position:absolute;left:-30px;top:-20px;width:140px;height:140px;
    background:radial-gradient(circle at 30% 30%, rgba(0,255,170,0.06), transparent 30%);
    transform:rotate(20deg);
  }}
  .logo-text{{font-weight:800;color:#00ffd6;font-size:20px;text-shadow:0 0 8px rgba(0,255,214,0.06)}}

  h1{{font-size:20px;color:#00ffd6;margin:0}}
  p.lead{{color:#9fb3c2;margin-top:6px}}

  .grid {{
    display:grid;
    grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
    gap:14px;
    margin-top:20px;
  }}

  .card {{
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    padding:18px;border-radius:12px;border:1px solid rgba(255,255,255,0.02);
    transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
    cursor:pointer;
  }}
  .card:hover{{ transform: translateY(-6px); box-shadow: 0 12px 30px rgba(0,255,180,0.06); background: rgba(255,255,255,0.03)}}
  .card h3{{margin-bottom:8px;color:#e8fffb}}
  .card p{{color:#9fb3c2;font-size:14px;line-height:1.45}}

  .cta-row{{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px;align-items:center}}
  .btn {{
    display:inline-flex;align-items:center;gap:8px;
    padding:12px 16px;border-radius:12px;text-decoration:none;
    font-weight:700;color:#071025;background:#00ffd6;border:none;cursor:pointer;
    box-shadow:0 10px 30px rgba(0,255,214,0.06);
    transition: transform .14s ease, box-shadow .14s ease, opacity .14s;
  }}
  .btn.ghost{{background:transparent;color:#9fb3c2;border:1px solid rgba(255,255,255,0.03)}}
  .btn:hover{{transform:translateY(-4px)}}

  .links { margin-top:18px; display:flex; gap:10px; flex-wrap:wrap; }
  .links a { text-decoration:none; padding:10px 12px; border-radius:10px; background: rgba(255,255,255,0.02); color:#cfeeea; font-weight:700; }

  footer { margin-top:22px; color:#7f9aa3; font-size:13px; text-align:center; }

  /* floating glow */
  .glow {{
    position:absolute;right:28px;top:28px;width:220px;height:220px;border-radius:50%;
    filter: blur(60px); opacity:0.25; background: radial-gradient(circle,#00ffd6 0%, transparent 40%);
    transform: translateZ(0);
  }}

  @media (max-width:560px) {{
    .top {{flex-direction:row;gap:12px}}
    .badge{{width:56px;height:56px}}
  }}
</style>
</head>
<body>
  <div class="panel">
    <div style="position:relative">
      <div class="glow"></div>
      <div class="top">
        <div class="badge"><div class="logo-text">HCO</div></div>
        <div style="flex:1">
          <h1>Welcome to Hackers Colony — Hacking Portal</h1>
          <p class="lead">Ethical learning, practice labs & community | Only test on systems you own or have permission to test.</p>
        </div>
      </div>

      <div class="grid" style="margin-top:20px">
        <div class="card" onclick="location.href='/learn'">
          <h3>📚 Learn Hacking</h3>
          <p>Guided learning path, foundational topics and recommended courses.</p>
        </div>

        <div class="card" onclick="location.href='/labs'">
          <h3>🧪 Practice Labs</h3>
          <p>Start safe labs (TryHackMe, Juice Shop) and local vulnerable VMs in isolated environments.</p>
        </div>

        <div class="card" onclick="location.href='/tutorials'">
          <h3>🎯 Tutorials</h3>
          <p>Step-by-step tutorials and curated YouTube lessons to follow along.</p>
        </div>

        <div class="card" onclick="location.href='/tools'">
          <h3>🛠 Tools & Guides</h3>
          <p>Learn how to use Nmap, Wireshark, Burp, and defensive tooling responsibly.</p>
        </div>

        <div class="card" onclick="location.href='/ctf'">
          <h3>🏁 CTF Exercises</h3>
          <p>Beginner CTFs, challenges and walkthroughs to build practical skills.</p>
        </div>
      </div>

      <div class="cta-row">
        <a class="btn" href="/join/telegram" target="_blank">Join Telegram</a>
        <a class="btn" href="/join/whatsapp" target="_blank" style="background:#25D366;color:#02120b">Join WhatsApp</a>
        <a class="btn ghost" href="/join/youtube" target="_blank">Watch Tutorials</a>
        <a class="btn ghost" href="{WEBSITE_LINK}" target="_blank">Official Website</a>
      </div>

      <div class="links">
        <a href="/download/cheatsheet">Download Cheat-sheet</a>
        <a href="/contact">Contact</a>
      </div>

      <footer>Made with ❤️ by Hackers Colony — Educational & ethical use only.</footer>
    </div>
  </div>

<script>
  // tiny animation: pulse glow
  const glow = document.querySelector('.glow');
  let tick = 0;
  setInterval(()=>{ tick += 0.02; glow.style.opacity = 0.18 + Math.sin(tick)*0.03; }, 50);
</script>
</body>
</html>
"""

# ---------- Subpages templates ----------
SUB_TEMPLATE = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{{font-family:Inter,system-ui;background:#020615;color:#e6eef6;padding:22px}}a{{color:#00ffd6}}</style></head>
<body>
  <h2>{title}</h2>
  <div>{html}</div>
  <p style="margin-top:18px"><a href="/">← Back to Portal</a></p>
</body></html>
"""

CHEATSHEET_TEXT = """HCO Terminal - Beginner Cheat-sheet

1) Start Juice Shop (Docker):
   docker run --rm -p 3000:3000 bkimminich/juice-shop

2) Simple nmap:
   nmap -sC -sV <target>

3) Save a web page:
   wget -k -p http://<target>/

4) Always use isolated VMs or cloud hosts you control.
5) Only test systems you own or have permission to test.
"""

# ---------- Routes ----------
from flask import send_file, request, redirect, url_for, render_template_string
from io import BytesIO
import json
JOIN_LOG = "join_clicks.log"

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/learn")
def learn():
    html = "<p>Recommended start: TryHackMe beginner path, networking basics, Linux commands, HTTP fundamentals.</p>"
    html += "<ul><li><a href='https://tryhackme.com' target='_blank'>TryHackMe</a></li><li><a href='https://developer.mozilla.org' target='_blank'>MDN Web Docs</a></li></ul>"
    return render_template_string(SUB_TEMPLATE.format(title="Learn Hacking", html=html))

@app.route("/labs")
def labs():
    html = "<p>Run Juice Shop locally with Docker or use TryHackMe/HackTheBox labs. Example:</p><pre>docker run --rm -p 3000:3000 bkimminich/juice-shop</pre>"
    return render_template_string(SUB_TEMPLATE.format(title="Practice Labs", html=html))

@app.route("/tutorials")
def tutorials():
    html = "<p>Curated playlists and hands-on walkthroughs. <a href='{0}' target='_blank'>YouTube Channel</a></p>".format(YOUTUBE_LINK)
    return render_template_string(SUB_TEMPLATE.format(title="Tutorials", html=html))

@app.route("/tools")
def tools():
    html = "<p>Overview of useful tools: <strong>nmap</strong>, <strong>wireshark</strong>, <strong>burp</strong>. Always use safely.</p>"
    return render_template_string(SUB_TEMPLATE.format(title="Tools & Guides", html=html))

@app.route("/ctf")
def ctf():
    html = "<p>Start with beginner CTFs on TryHackMe. Practice web, forensics, and crypto categories.</p>"
    return render_template_string(SUB_TEMPLATE.format(title="CTF / Exercises", html=html))

@app.route("/download/cheatsheet")
def download_cheatsheet():
    bio = BytesIO()
    bio.write(CHEATSHEET_TEXT.encode('utf-8'))
    bio.seek(0)
    return send_file(bio, download_name="hco_cheatsheet.txt", as_attachment=True, mimetype="text/plain")

def log_join(platform, target):
    try:
        with open(JOIN_LOG, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} JOIN {platform} -> {target} from {request.remote_addr}\\n")
    except Exception:
        pass

@app.route("/join/<platform>")
def join(platform):
    platform = platform.lower()
    if platform == "telegram":
        target = TELEGRAM_LINK
    elif platform == "whatsapp":
        target = WHATSAPP_LINK
    elif platform in ("youtube","yt"):
        target = YOUTUBE_LINK
    else:
        return redirect(url_for("home"))
    try:
        log_join(platform, target)
    except Exception:
        pass
    # Use a tiny redirect HTML so mobile apps can pick the link
    redirect_html = f"""
    <!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>Opening…</title></head><body style='background:#000;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh'>
    <script>window.location.replace("{target}");</script>
    <div style='text-align:center'><p>Opening {platform}…</p><p><a href='{target}' target='_blank'>Click here if not redirected</a></p></div>
    </body></html>
    """
    return redirect_html

# ---------- Open URL helper (Termux friendly) ----------
def open_url(url):
    # 1) termux-open-url
    if shutil.which("termux-open-url"):
        try:
            subprocess.run(["termux-open-url", url], check=False)
            return True
        except Exception:
            pass
    # 2) Android am
    if shutil.which("am"):
        try:
            subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", url], check=False)
            return True
        except Exception:
            pass
    # 3) fallback
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False

# ---------- Server runner ----------
def run_server():
    # Serve on localhost by default
    app.run(host=HOST, port=PORT, debug=False, threaded=True)

def start():
    url = f"http://{HOST}:{PORT}/"
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    # give server a moment
    time.sleep(0.8)
    print(f"[+] {APP_NAME} running at {url}")
    opened = open_url(url)
    if opened:
        print("[+] Attempted to open your browser/app. If nothing opened, copy the URL below to your browser:")
    else:
        print("[!] Could not open browser automatically. Open this URL in your browser:")
    print("    " + url)

if __name__ == "__main__":
    os.system("clear")
    print(f"Starting {APP_NAME} — Hackers Colony Portal")
    if not shutil.which("python") and not shutil.which("python3"):
        print("[!] Warning: 'python' not found in PATH")
    start()
    try:
        # keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down. Bye.")
        sys.exit(0)
