#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCO Terminal (single-file) — v1.1
Author: Azhar (Hackers Colony)
Filename suggestion: hco_terminal.py
Description:
    - Single-file Flask portal to run in Termux (or any Python environment)
    - Automatically attempts to open mobile browser to the local portal
    - Starts a small site with:
        * Welcome banner / ethical disclaimer
        * Large action buttons (Learn, Labs, Tutorials, Tools, CTF)
        * Clickable join links: WhatsApp group, Telegram group, (optional) YouTube
    - Configurable links at the top of this file
    - Intended for legal / educational purposes only

Usage (Termux):
    pkg update && pkg install python
    pip install flask
    python3 hco_terminal.py

License: MIT (short header included)
"""

from flask import Flask, render_template_string
import threading
import subprocess
import shutil
import time
import webbrowser
import os
import sys
from datetime import datetime

# ------------------------
# Configuration - Edit these
# ------------------------
APP_NAME = "HCO Terminal"
HOST = "127.0.0.1"      # keep local by default; change to "0.0.0.0" to expose on LAN
PORT = 8080

# Community links - replace with your actual invite links
WHATSAPP_LINK = "https://chat.whatsapp.com/BHwZHVntVicI8zdmfbJoQV?mode=wwt"
TELEGRAM_LINK = "https://t.me/HackersColony"
YOUTUBE_LINK = "https://youtube.com/@hackers_colony_tech?si=pWiyLolJ5323Q7Or"  # optional

OPEN_TIMEOUT = 0.8  # seconds to wait before trying to open browser

# ------------------------
# Minimal license text (for GitHub file)
# ------------------------
MIT_LICENSE_TEXT = """MIT License

Copyright (c) {year} Azhar

Permission is hereby granted, free of charge, to any person obtaining a copy...
""".format(year=datetime.utcnow().year)

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
          <a class="join-btn" href="{whatsapp}" target="_blank">🔗 Join WhatsApp Group</a>
          <a class="join-btn" href="{telegram}" target="_blank">🔗 Join Telegram</a>
          <a class="join-btn" href="{youtube}" target="_blank">▶ Subscribe on YouTube</a>
        </div>
        <p class="small" style="margin-top:8px;">Tapping these links will open the corresponding app if installed or open the link in your browser.</p>
      </div>
    </div>

    <div class="card">
      <h3>Quick links</h3>
      <ul class="links">
        <li><a href="https://tryhackme.com" target="_blank">TryHackMe — Hands-on rooms</a></li>
        <li><a href="https://owasp.org/www-project-juice-shop/" target="_blank">OWASP Juice Shop — Vulnerable web app demo</a></li>
        <li><a href="https://www.hackthebox.com" target="_blank">Hack The Box — Practice labs</a></li>
        <li><a href="https://developer.mozilla.org" target="_blank">MDN — Web fundamentals</a></li>
      </ul>
      <p class="small">Made with ❤ by Hackers Colony — For education only.</p>
    </div>

    <footer>{app_name} — Run in Termux: <code>python3 hco_terminal.py</code></footer>
  </div>
</body>
</html>
""".format(app_name=APP_NAME, whatsapp=WHATSAPP_LINK, telegram=TELEGRAM_LINK, youtube=YOUTUBE_LINK)

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
<p><a href="/">← Back</a></p></body></html>
"""

LABS_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Labs</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>Practice Labs — Safe Options</h2>
<ol>
<li>TryHackMe / HackTheBox (online, legal CTF platforms)</li>
<li>OWASP Juice Shop — run locally in an isolated VM or Docker</li>
<li>Vulnerable VM images (Metasploitable) in an isolated host or VM</li>
</ol>
<p><strong>Note:</strong> Always isolate vulnerable services from your main network.</p>
<p><a href="/">← Back</a></p></body></html>
"""

TUTORIALS_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tutorials</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>Tutorials</h2>
<ul>
<li>Web security fundamentals</li>
<li>Network basics & packet capture (Wireshark)</li>
<li>Secure coding & defensive practices</li>
</ul>
<p><a href="/">← Back</a></p></body></html>
"""

TOOLS_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tools</title></head>
<body style="background:#071126;color:#e6eef6;font-family:system-ui;padding:18px">
<h2>Tools & Guides</h2>
<ul>
<li>nmap — safe scanning (only with permission)</li>
<li>Wireshark — packet analysis (learn on test captures)</li>
<li>Python, Git, and web frameworks for defensive tooling</li>
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
<p><a href="/">← Back</a></p></body></html>
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
    # Note: debug=False to avoid auto-reloader spawning multiple threads
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
