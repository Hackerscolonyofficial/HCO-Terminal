#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCO Terminal (single-file) — v1.2
Author: Azhar (Hackers Colony)
Filename: hco_terminal.py

Improvements in v1.2:
 - Join links use redirect endpoints (/join/telegram, /join/whatsapp, /join/youtube)
 - Join clicks are logged to join_clicks.log
 - Pages contain more actionable items (buttons, sample commands, downloadable cheat-sheet)
 - All in a single file for GitHub

Usage (Termux):
    pkg update && pkg install python
    pip install flask
    python3 hco_terminal.py
"""

from flask import Flask, render_template_string, redirect, url_for, send_file, request
import threading
import subprocess
import shutil
import time
import webbrowser
import os
import sys
from datetime import datetime
from io import BytesIO

# ------------------------
# Configuration - Edit these
# ------------------------
APP_NAME = "HCO Terminal"
HOST = "127.0.0.1"      # keep local by default; change to "0.0.0.0" to expose on LAN
PORT = 8080

# Community links - replace with your actual invite links where needed
WHATSAPP_LINK = "https://chat.whatsapp.com/BHwZHVntVicI8zdmfbJoQV?mode=wwt"  # REPLACE with your real invite
TELEGRAM_LINK = "https://t.me/HackersColony"
YOUTUBE_LINK = "https://youtube.com/@hackers_colony_tech?si=51CiCi_q1_CwiTnc"

OPEN_TIMEOUT = 0.8  # seconds to wait before trying to open browser
JOIN_LOG = "join_clicks.log"  # local file to store join clicks

# ------------------------
# Flask app and templates
# ------------------------
app = Flask(__name__)

MAIN_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{app_name} — Hacking Portal</title>
  <style>
    :root {{ --bg:#071126; --card:#0f1720; --accent:#ff4d4d; --muted:#9aa5b1; --glass: rgba(255,255,255,0.03); }}
    html,body{{height:100%;margin:0;padding:0;background:linear-gradient(180deg,#071126,#021018);font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial;color:#e6eef6}}
    .wrap{{max-width:980px;margin:18px auto;padding:18px}}
    header{{display:flex;align-items:center;gap:14px}}
    .logo{{width:64px;height:64px;border-radius:12px;background:var(--glass);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--accent);font-size:24px}}
    h1{{margin:0;font-size:20px}}
    .lead{{color:var(--muted);margin-top:6px}}
    .card{{background:rgba(255,255,255,0.03);padding:18px;border-radius:12px;margin-top:16px;box-shadow:0 8px 30px rgba(2,6,23,0.6)}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:12px}}
    .btn{{display:block;padding:14px;border-radius:10px;text-decoration:none;color:white;font-weight:700;text-align:center;background:linear-gradient(90deg,var(--accent),#fb8b24)}}
    a{{color:inherit}}
    .subtitle{{color:var(--muted);font-size:13px;margin-top:12px}}
    footer{{color:var(--muted);margin-top:18px;font-size:13px;text-align:center}}
    ul.links{{padding-left:18px}}
    .small{{font-size:13px;color:var(--muted)}}
    .join-grid{{display:flex;flex-direction:column;gap:8px;margin-top:12px}}
    .join-btn{{display:inline-block;padding:10px;border-radius:10px;text-decoration:none;color:#0b1220;font-weight:700;text-align:center;background:#fff}}
    .inline-link{{display:inline-block;margin-right:8px;padding:8px 12px;border-radius:10px;background:#0f1720;color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,0.04)}}
    @media (max-width:420px){{ .wrap{{padding:12px}} }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="logo">HCO</div>
      <div>
        <h1>{app_name} — Hacking Portal</h1>
        <p class="lead">A safe starting place to learn ethical hacking & practice in legal, isolated labs.</p>
      </div>
    </header>

    <div class="card">
      <div style="background:#2b2f36;padding:10px;border-radius:8px;color:#ffd7d7"><strong>Ethical Use Only:</strong>
      Practice only on systems you own or have explicit permission to test. Illegal activity is not supported.</div>

      <div class="grid">
        <a class="btn" href="/learn">📚 Learn Hacking</a>
        <a class="btn" href="/labs">🧪 Practice Labs</a>
        <a class="btn" href="/tutorials">🎯 Tutorials</a>
        <a class="btn" href="/tools">🛠 Tools & Guides</a>
        <a class="btn" href="/ctf">🏁 CTF / Exercises</a>
      </div>

      <p class="subtitle">Tip: Use TryHackMe, Hack The Box, or local isolated VMs (Metasploitable, Juice Shop). Keep practice networks isolated.</p>

      <div style="margin-top:14px">
        <h3>Join our community</h3>
        <div class="join-grid">
          <a class="join-btn" href="/join/whatsapp" target="_blank">🔗 Join WhatsApp Group</a>
          <a class="join-btn" href="/join/telegram" target="_blank">🔗 Join Telegram</a>
          <a class="join-btn" href="/join/youtube" target="_blank">▶ Subscribe on YouTube</a>
        </div>
        <p class="small" style="margin-top:8px;">Tapping these links will open the corresponding app if installed or open the link in your browser.</p>
      </div>
    </div>

    <div class="card">
      <h3>Quick links</h3>
      <ul class="links">
        <li><a class="inline-link" href="https://tryhackme.com" target="_blank">TryHackMe</a>
            <a class="inline-link" href="https://www.hackthebox.com" target="_blank">HackTheBox</a>
            <a class="inline-link" href="https://owasp.org" target="_blank">OWASP</a></li>
        <li style="margin-top:10px"><a href="/download/cheatsheet">Download beginner cheat-sheet (text)</a></li>
      </ul>
      <p class="small">Made with ❤ by Hackers Colony — For education only.</p>
    </div>

    <footer>{app_name} — Run in Termux: <code>python3 hco_terminal.py</code></footer>
  </div>
</body>
</html>
""".format(app_name=APP_NAME)

LEARN_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Learn Hacking</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>Learn Hacking — Safe Resources</h2>
<ul>
<li><a href="https://tryhackme.com" target="_blank">TryHackMe — Guided hands-on learning</a></li>
<li><a href="https://www.hackthebox.com" target="_blank">Hack The Box — Practice labs</a></li>
<li><a href="https://owasp.org" target="_blank">OWASP — Web app security</a></li>
<li><a href="https://developer.mozilla.org" target="_blank">MDN — Web fundamentals</a></li>
</ul>
<hr>
<h3>Beginner checklist</h3>
<ol>
<li>Create accounts on TryHackMe / HackTheBox.</li>
<li>Learn HTTP basics (GET/POST) and HTML forms.</li>
<li>Practice safe labs inside a VM or cloud instance you control.</li>
</ol>
<p><a href="/">← Back</a></p></body></html>
"""

LABS_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Labs</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>Practice Labs — Safe Options</h2>
<ol>
<li>TryHackMe / HackTheBox (online, legal CTF platforms)</li>
<li>OWASP Juice Shop — run locally (Docker recommended)</li>
<li>Vulnerable VM images (Metasploitable) inside VirtualBox/VMware</li>
</ol>

<h3>Quick lab commands</h3>
<ul>
<li>Run Juice Shop via Docker: <code>docker run --rm -p 3000:3000 bkimminich/juice-shop</code></li>
<li>Download Metasploitable (run in isolated VM)</li>
<li>Start a browser and point to local lab URLs</li>
</ul>

<p><a href="/">← Back</a></p></body></html>
"""

TUTORIALS_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tutorials</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>Tutorials</h2>
<ul>
<li>Web security fundamentals — Cross-Site Scripting, SQLi</li>
<li>Network basics & packet capture (Wireshark)</li>
<li>Secure coding & defensive practices</li>
</ul>

<h3>Sample study plan (4 weeks)</h3>
<ol>
<li>Week 1: Networking & Linux basics</li>
<li>Week 2: Web fundamentals and HTTP</li>
<li>Week 3: Web vulns (XSS, SQLi) on Juice Shop</li>
<li>Week 4: CTF practice & writeups</li>
</ol>

<p><a href="/">← Back</a></p></body></html>
"""

TOOLS_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tools</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>Tools & Guides</h2>
<ul>
<li><strong>nmap</strong> — network discovery (only with permission)</li>
<li><strong>Wireshark</strong> — packet analysis (learn on test captures)</li>
<li><strong>Python, Git</strong> — scripting & code management</li>
</ul>

<h3>Example commands</h3>
<ul>
<li>Simple nmap: <code>nmap -sC -sV TARGET</code></li>
<li>Save web page: <code>wget -k -p http://target/</code></li>
</ul>

<p><a href="/">← Back</a></p></body></html>
"""

CTF_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>CTF</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>CTF / Exercises</h2>
<p>Begin with easy rooms on TryHackMe. Explore:</p>
<ul>
<li>Web exploitation (beginner)</li>
<li>Forensics & steganography</li>
<li>Crypto & reversing (intro)</li>
</ul>

<h3>Start a simple challenge locally</h3>
<p>Use Juice Shop Docker instance and try to find simple flags on the app.</p>

<p><a href="/">← Back</a></p></body></html>
"""

REDIRECTING_HTML = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Redirecting…</title>
<style>body{{background:#071126;color:#e6eef6;font-family:system-ui;padding:18px}}</style>
</head>
<body>
  <h3>Opening external link…</h3>
  <p>If the link doesn't open automatically, <a id="link" href="{target}" target="_blank">click here</a>.</p>
  <script>
    // try to open immediately
    window.location.href = "{target}";
  </script>
</body></html>
"""

CHEATSHEET_TEXT = """HCO Terminal - Beginner cheat-sheet

1) Start Juice Shop (Docker):
   docker run --rm -p 3000:3000 bkimminich/juice-shop

2) Useful nmap:
   nmap -sC -sV <target>

3) Save a web page:
   wget -k -p http://<target>/

4) Keep everything in an isolated VM or sandbox.
5) Only test systems you own or have permission to test.
"""

# ------------------------
# Routes
# ------------------------
@app.route("/")
def index():
    return MAIN_HTML

@app.route("/learn")
def learn():
    return LEARN_HTML

@app.route("/labs")
def labs():
    return LABS_HTML

@app.route("/tutorials")
def tutorials():
    return TUTORIALS_HTML

@app.route("/tools")
def tools():
    return TOOLS_HTML

@app.route("/ctf")
def ctf():
    return CTF_HTML

@app.route("/download/cheatsheet")
def download_cheatsheet():
    # serve a small text file for quick download
    bio = BytesIO()
    bio.write(CHEATSHEET_TEXT.encode("utf-8"))
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name="hco_cheatsheet.txt", mimetype="text/plain")

# Join redirect endpoints (ensures link is present and logged)
def log_join(platform: str, target: str):
    try:
        with open(JOIN_LOG, "a") as f:
            f.write(f"{datetime.utcnow().isoformat()} JOIN {platform} -> {target} | from: {request.remote_addr}\\n")
    except Exception:
        pass

@app.route("/join/<platform>")
def join(platform):
    # safe map
    platform = platform.lower()
    if platform == "telegram":
        target = TELEGRAM_LINK
    elif platform == "whatsapp":
        target = WHATSAPP_LINK
    elif platform in ("youtube", "yt"):
        target = YOUTUBE_LINK
    else:
        # unknown -> back to home
        return redirect(url_for("index"))
    # log and redirect via a redirecting page (helps mobile open apps)
    try:
        log_join(platform, target)
    except Exception:
        pass
    return render_template_string(REDIRECTING_HTML.format(target=target))

# ------------------------
# Helpers to open the URL on Android/Termux
# ------------------------
def open_url_on_android(url: str) -> bool:
    """
    Try to open URL using:
      1) termux-open-url (preferred on Termux)
      2) am start (Android intent)
      3) webbrowser fallback
    Returns True if an attempt was made.
    """
    # 1) termux-open-url
    if shutil.which("termux-open-url"):
        try:
            subprocess.run(["termux-open-url", url], check=False)
            return True
        except Exception:
            pass
    # 2) am start (Activity Manager)
    if shutil.which("am"):
        try:
            subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", url], check=False)
            return True
        except Exception:
            pass
    # 3) webbrowser fallback
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False

# ------------------------
# Server start
# ------------------------
def run_server(host: str, port: int):
    app.run(host=host, port=port, debug=False, threaded=True)

def start_and_open(host: str = HOST, port: int = PORT):
    url = f"http://{host}:{port}/"
    thread = threading.Thread(target=run_server, args=(host, port), daemon=True)
    thread.start()
    time.sleep(OPEN_TIMEOUT)
    print(f"[+] {APP_NAME} running at {url}")
    tried = open_url_on_android(url)
    if tried:
        print("[+] Attempted to open your browser/app. If nothing opened, copy the URL below into your browser:")
    else:
        print("[!] Could not open browser automatically. Please open the URL manually:")
    print(f"    {url}")
    print("[i] Press Ctrl+C to stop the portal.")

# ------------------------
# Simple dependency check and CLI
# ------------------------
def check_dependencies() -> bool:
    try:
        import flask  # noqa: F401
    except Exception:
        print("[!] Flask is not installed. Install with: pip install flask")
        return False
    return True

def print_header():
    print("=" * 58)
    print(f"{APP_NAME} — Single-file portal (Educational use only)")
    print("Author: Hackers Colony (Azhar)")
    print("=" * 58)

def main():
    print_header()
    if not check_dependencies():
        sys.exit(1)

    host = HOST
    port = PORT
    # allow exposing on LAN with CLI option
    if len(sys.argv) > 1 and "--host" in sys.argv and "0.0.0.0" in sys.argv:
        host = "0.0.0.0"
        print("[!] Binding to 0.0.0.0 - portal will be accessible on your LAN (use with caution).")

    try:
        start_and_open(host, port)
        # keep alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] Shutting down HCO Terminal. Bye.")
        os._exit(0)

if __name__ == "__main__":
    main()
