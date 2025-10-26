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

from flask import Flask, render_template_string, request, redirect, url_for, send_file
import threading, subprocess, shutil, time, webbrowser, os, sys
import json
from datetime import datetime

# ---------- Config ----------
APP_NAME = "HCO Terminal"
HOST = "127.0.0.1"
PORT = 8080

TELEGRAM_LINK = "https://t.me/HackersColony"
WHATSAPP_LINK = "https://chat.whatsapp.com/BHwZHVntVicI8zdmfbJoQV"
YOUTUBE_LINK  = "https://youtube.com/@hackers_colony_tech?si=51CiCi_q1_CwiTnc"
WEBSITE_LINK  = "https://hackerscolonyofficial.blogspot.com/?m=1"
LEARN_LINK    = "https://tryhackme.com"

# ---------- Flask app ----------
app = Flask(__name__)

# Store active processes
active_processes = {}

HTML = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>''' + APP_NAME + ''' — Hackers Colony Portal</title>
<link rel="icon" href="data:,">
<style>
  /* Reset */
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{height:100%}
  body {
    font-family: Inter, "Segoe UI", Roboto, system-ui, -apple-system, sans-serif;
    background: radial-gradient(1200px 600px at 10% 10%, #07102a 0%, #02020a 35%, #000 100%);
    color:#e6eef6;
    -webkit-font-smoothing:antialiased;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:24px;
  }

  .panel {
    width:100%;
    max-width:980px;
    border-radius:16px;
    padding:28px;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    box-shadow: 0 10px 40px rgba(2,6,23,0.7), inset 0 1px 0 rgba(255,255,255,0.02);
    backdrop-filter: blur(6px);
  }

  .top {
    display:flex;
    align-items:center;
    gap:18px;
  }
  .badge {
    width:72px;height:72px;border-radius:14px;
    display:flex;align-items:center;justify-content:center;
    background: linear-gradient(135deg,#09182b,#05283a);
    box-shadow: 0 6px 20px rgba(0,170,150,0.08);
    position:relative;
    overflow:hidden;
  }
  .badge:after{
    content:"";
    position:absolute;left:-30px;top:-20px;width:140px;height:140px;
    background:radial-gradient(circle at 30% 30%, rgba(0,255,170,0.06), transparent 30%);
    transform:rotate(20deg);
  }
  .logo-text{font-weight:800;color:#00ffd6;font-size:20px;text-shadow:0 0 8px rgba(0,255,214,0.06)}

  h1{font-size:20px;color:#00ffd6;margin:0}
  p.lead{color:#9fb3c2;margin-top:6px}

  .grid {
    display:grid;
    grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
    gap:14px;
    margin-top:20px;
  }

  .card {
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    padding:18px;border-radius:12px;border:1px solid rgba(255,255,255,0.02);
    transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
    cursor:pointer;
  }
  .card:hover{ transform: translateY(-6px); box-shadow: 0 12px 30px rgba(0,255,180,0.06); background: rgba(255,255,255,0.03)}
  .card h3{margin-bottom:8px;color:#e8fffb}
  .card p{color:#9fb3c2;font-size:14px;line-height:1.45}

  .cta-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px;align-items:center}
  .btn {
    display:inline-flex;align-items:center;gap:8px;
    padding:12px 16px;border-radius:12px;text-decoration:none;
    font-weight:700;color:#071025;background:#00ffd6;border:none;cursor:pointer;
    box-shadow:0 10px 30px rgba(0,255,214,0.06);
    transition: transform .14s ease, box-shadow .14s ease, opacity .14s;
  }
  .btn.ghost{background:transparent;color:#9fb3c2;border:1px solid rgba(255,255,255,0.03)}
  .btn:hover{transform:translateY(-4px)}

  .links { margin-top:18px; display:flex; gap:10px; flex-wrap:wrap; }
  .links a { text-decoration:none; padding:10px 12px; border-radius:10px; background: rgba(255,255,255,0.02); color:#cfeeea; font-weight:700; }

  footer { margin-top:22px; color:#7f9aa3; font-size:13px; text-align:center; }

  /* floating glow */
  .glow {
    position:absolute;right:28px;top:28px;width:220px;height:220px;border-radius:50%;
    filter: blur(60px); opacity:0.25; background: radial-gradient(circle,#00ffd6 0%, transparent 40%);
    transform: translateZ(0);
  }

  /* Terminal output */
  .terminal {
    background: #0a0e1a;
    border: 1px solid rgba(0,255,214,0.1);
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    color: #00ffd6;
    max-height: 300px;
    overflow-y: auto;
    white-space: pre-wrap;
  }

  .status {
    padding: 8px 12px;
    border-radius: 6px;
    margin: 10px 0;
    font-size: 14px;
  }
  .status.running { background: rgba(0,255,214,0.1); color: #00ffd6; }
  .status.stopped { background: rgba(255,0,0,0.1); color: #ff4444; }

  @media (max-width:560px) {
    .top {flex-direction:row;gap:12px}
    .badge{width:56px;height:56px}
  }
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
        <a class="btn ghost" href="''' + WEBSITE_LINK + '''" target="_blank">Official Website</a>
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
</html>'''

# ---------- Utility Functions ----------
def check_tool_installed(tool_name):
    """Check if a tool is installed on the system"""
    return shutil.which(tool_name) is not None

def run_command(cmd, timeout=30):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'output': '', 'error': 'Command timed out', 'returncode': -1}
    except Exception as e:
        return {'success': False, 'output': '', 'error': str(e), 'returncode': -1}

def create_cheatsheet():
    """Create a basic ethical hacking cheatsheet"""
    content = """HCO Ethical Hacking Cheat Sheet
========================

Basic Commands:
---------------
• nmap -sS -sV -O target.com
• nikto -h target.com
• dirb http://target.com

Common Ports:
-------------
21 - FTP, 22 - SSH, 80 - HTTP, 443 - HTTPS
3306 - MySQL, 5432 - PostgreSQL

Web Testing:
------------
• Always get permission first
• Use Burp Suite for web app testing
• Test for SQL injection, XSS, CSRF

Legal Notice:
-------------
Only test systems you own or have explicit written permission to test.
Unauthorized access is illegal and unethical.

Stay Ethical! 🛡️
"""
    filename = "hco_cheatsheet.txt"
    with open(filename, 'w') as f:
        f.write(content)
    return filename

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/join/<platform>')
def join_platform(platform):
    platforms = {
        'telegram': TELEGRAM_LINK,
        'whatsapp': WHATSAPP_LINK,
        'youtube': YOUTUBE_LINK
    }
    link = platforms.get(platform)
    if link:
        return redirect(link)
    return redirect('/')

@app.route('/learn')
def learn():
    content = """
    <div class="panel">
        <div style="position:relative">
            <a href="/" style="color:#00ffd6; text-decoration:none;">← Back</a>
            <h1 style="margin:20px 0;color:#00ffd6">📚 Learn Ethical Hacking</h1>
            
            <div class="card">
                <h3>🔰 Beginner Path</h3>
                <p>1. Networking Fundamentals<br>2. Linux Basics<br>3. Programming (Python/Bash)<br>4. Security Concepts</p>
            </div>
            
            <div class="card">
                <h3>🎯 Intermediate Topics</h3>
                <p>• Web Application Security<br>• Network Penetration Testing<br>• Wireless Security<br>• Social Engineering</p>
            </div>
            
            <div class="card">
                <h3>🏆 Advanced Skills</h3>
                <p>• Reverse Engineering<br>• Exploit Development<br>• Digital Forensics<br>• Malware Analysis</p>
            </div>
            
            <div class="terminal">
# Recommended Learning Resources:
- TryHackMe: https://tryhackme.com
- Hack The Box: https://hackthebox.com
- Cybrary: https://cybrary.it
- HCO YouTube Tutorials
            </div>
            
            <div style="margin-top:20px">
                <a class="btn" href="https://tryhackme.com" target="_blank">Start Learning</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', 'Learn - HCO Terminal'))

@app.route('/labs')
def labs():
    # Check available tools
    tools_status = {
        'docker': check_tool_installed('docker'),
        'python3': check_tool_installed('python3'),
        'git': check_tool_installed('git')
    }
    
    tools_text = "\n".join([f"{'✅' if status else '❌'} {tool}" for tool, status in tools_status.items()])
    
    content = f"""
    <div class="panel">
        <div style="position:relative">
            <a href="/" style="color:#00ffd6; text-decoration:none;">← Back</a>
            <h1 style="margin:20px 0;color:#00ffd6">🧪 Practice Labs</h1>
            
            <div class="terminal">
# Available Tools:
{tools_text}

# Safe Practice Environments:
1. TryHackMe - Beginner friendly
2. Hack The Box - Intermediate/Advanced
3. VulnHub VMs - Realistic scenarios
4. OWASP Juice Shop - Web app practice
            </div>
            
            <div class="card" onclick="location.href='/start_lab/owasp'">
                <h3>🛡️ OWASP Juice Shop</h3>
                <p>Modern vulnerable web application for learning web security.</p>
            </div>
            
            <div class="card" onclick="location.href='/start_lab/metasploitable'">
                <h3>🎯 Metasploitable</h3>
                <p>Intentionally vulnerable VM for penetration testing practice.</p>
            </div>
            
            <div style="margin-top:20px">
                <a class="btn" href="https://tryhackme.com" target="_blank">TryHackMe</a>
                <a class="btn ghost" href="https://www.hackthebox.com" target="_blank">HackTheBox</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', 'Labs - HCO Terminal'))

@app.route('/start_lab/<lab_name>')
def start_lab(lab_name):
    output = ""
    if lab_name == "owasp":
        output = """
# To run OWASP Juice Shop locally:

# Using Docker (recommended):
docker pull bkimminich/juice-shop
docker run -d -p 3000:3000 bkimminich/juice-shop

# Then open: http://localhost:3000

# Or use the online version:
# https://juice-shop.herokuapp.com
        """
    elif lab_name == "metasploitable":
        output = """
# Metasploitable Setup:

1. Download from:
   https://sourceforge.net/projects/metasploitable/

2. Run in VirtualBox/VMware

3. Login credentials:
   msfadmin:msfadmin

⚠️  WARNING: Only run on isolated network!
        """
    
    content = f"""
    <div class="panel">
        <div style="position:relative">
            <a href="/labs" style="color:#00ffd6; text-decoration:none;">← Back to Labs</a>
            <h1 style="margin:20px 0;color:#00ffd6">🚀 Starting {lab_name.title()}</h1>
            
            <div class="terminal">{output}</div>
            
            <div style="margin-top:20px">
                <a class="btn" href="/labs">More Labs</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', f'Starting {lab_name} - HCO Terminal'))

@app.route('/tutorials')
def tutorials():
    content = """
    <div class="panel">
        <div style="position:relative">
            <a href="/" style="color:#00ffd6; text-decoration:none;">← Back</a>
            <h1 style="margin:20px 0;color:#00ffd6">🎯 Tutorials & Guides</h1>
            
            <div class="card" onclick="window.open('/join/youtube', '_blank')">
                <h3>📹 Video Tutorials</h3>
                <p>Step-by-step hacking tutorials on YouTube covering various topics.</p>
            </div>
            
            <div class="card">
                <h3>📖 Written Guides</h3>
                <p>Detailed articles and walkthroughs for different hacking techniques.</p>
            </div>
            
            <div class="terminal">
# Popular Tutorial Topics:

1. Setting Up Kali Linux
2. Basic Nmap Scanning
3. Web Application Testing
4. Wireless Network Security
5. Social Engineering Awareness
6. Cryptography Basics
7. Digital Forensics Introduction

# Quick Commands Tutorial:
nmap -A -T4 target.com  # Aggressive scan
sqlmap -u "http://site.com/page?param=1" --dbs
burpsuite &  # Start Burp Suite
            </div>
            
            <div style="margin-top:20px">
                <a class="btn" href="/join/youtube" target="_blank">Watch Videos</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', 'Tutorials - HCO Terminal'))

@app.route('/tools')
def tools():
    # Check common tools
    tools = ['nmap', 'wireshark', 'python3', 'git', 'curl', 'nikto', 'sqlmap']
    tools_status = {tool: check_tool_installed(tool) for tool in tools}
    
    tools_list = "\n".join([f"{'✅' if status else '❌'} {tool}" for tool, status in tools_status.items()])
    
    content = f"""
    <div class="panel">
        <div style="position:relative">
            <a href="/" style="color:#00ffd6; text-decoration:none;">← Back</a>
            <h1 style="margin:20px 0;color:#00ffd6">🛠 Tools & Guides</h1>
            
            <div class="terminal">
# Installed Tools Check:
{tools_list}

# Essential Tools Guide:

• Nmap - Network scanning
  nmap -sS -sV -O target.com

• Wireshark - Packet analysis
  wireshark &  # GUI version

• Nikto - Web server scanner
  nikto -h http://target.com

• SQLMap - SQL injection tool
  sqlmap -u "http://site.com/page?id=1"
            </div>
            
            <div class="card">
                <h3>📋 Tool Installation</h3>
                <p>sudo apt update && sudo apt install nmap wireshark nikto sqlmap</p>
            </div>
            
            <div style="margin-top:20px">
                <a class="btn" href="/download/cheatsheet">Download Cheat Sheet</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', 'Tools - HCO Terminal'))

@app.route('/ctf')
def ctf():
    content = """
    <div class="panel">
        <div style="position:relative">
            <a href="/" style="color:#00ffd6; text-decoration:none;">← Back</a>
            <h1 style="margin:20px 0;color:#00ffd6">🏁 CTF Exercises</h1>
            
            <div class="card">
                <h3>🔓 Beginner CTFs</h3>
                <p>• OverTheWire: Bandit, Natas<br>• PicoCTF<br>• TryHackMe Beginner Path</p>
            </div>
            
            <div class="card">
                <h3>⚡ Intermediate Challenges</h3>
                <p>• Hack The Box Starting Point<br>• VulnHub Machines<br>• CTFtime.org Events</p>
            </div>
            
            <div class="terminal">
# CTF Categories:

1. Web Exploitation
2. Cryptography
3. Reverse Engineering
4. Forensics
5. Binary Exploitation
6. Miscellaneous

# Getting Started:
- OverTheWire: https://overthewire.org
- PicoCTF: https://picoctf.org
- CTFtime: https://ctftime.org

# Practice Commands:
file challenge.bin      # Check file type
strings file.txt        # Extract strings
binwalk image.jpg       # Analyze firmware
            </div>
            
            <div style="margin-top:20px">
                <a class="btn" href="https://overthewire.org" target="_blank">OverTheWire</a>
                <a class="btn ghost" href="https://picoctf.org" target="_blank">PicoCTF</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', 'CTF - HCO Terminal'))

@app.route('/download/cheatsheet')
def download_cheatsheet():
    filename = create_cheatsheet()
    return send_file(filename, as_attachment=True, download_name='hco_ethical_hacking_cheatsheet.txt')

@app.route('/contact')
def contact():
    content = """
    <div class="panel">
        <div style="position:relative">
            <a href="/" style="color:#00ffd6; text-decoration:none;">← Back</a>
            <h1 style="margin:20px 0;color:#00ffd6">📞 Contact & Support</h1>
            
            <div class="card">
                <h3>📱 Social Media</h3>
                <p>• Telegram: @HackersColony<br>• YouTube: @hackers_colony_tech<br>• WhatsApp Group</p>
            </div>
            
            <div class="card">
                <h3>🌐 Website</h3>
                <p>https://hackerscolonyofficial.blogspot.com</p>
            </div>
            
            <div class="terminal">
# Important Notice:

This portal is for educational purposes only.
Always practice ethical hacking principles.

• Only test systems you own
• Get proper authorization
• Respect privacy and laws
• Help improve security

# Stay Legal, Stay Ethical! 🔐
            </div>
            
            <div style="margin-top:20px">
                <a class="btn" href="/join/telegram">Telegram</a>
                <a class="btn" href="/join/whatsapp">WhatsApp</a>
                <a class="btn ghost" href="/join/youtube">YouTube</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', 'Contact - HCO Terminal'))

@app.route('/system/check')
def system_check():
    """Check system tools and provide installation commands"""
    tools = ['python3', 'git', 'docker', 'nmap', 'wireshark', 'nikto']
    results = {}
    
    for tool in tools:
        results[tool] = check_tool_installed(tool)
    
    output = "System Tools Check:\n\n"
    for tool, installed in results.items():
        status = "✅ INSTALLED" if installed else "❌ MISSING"
        output += f"{status} {tool}\n"
    
    output += "\nInstall missing tools:\n"
    output += "sudo apt update && sudo apt install python3 git nmap wireshark nikto\n"
    output += "# Docker: curl -fsSL https://get.docker.com | sh\n"
    
    content = f"""
    <div class="panel">
        <div style="position:relative">
            <a href="/" style="color:#00ffd6; text-decoration:none;">← Back</a>
            <h1 style="margin:20px 0;color:#00ffd6">🖥️ System Check</h1>
            
            <div class="terminal">{output}</div>
            
            <div style="margin-top:20px">
                <a class="btn" href="/tools">Tools Guide</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(HTML.replace('</body>', f'{content}</body>').replace('HCO Terminal — Hackers Colony Portal', 'System Check - HCO Terminal'))

def open_browser():
    """Open web browser when server starts"""
    time.sleep(2)
    webbrowser.open(f'http://{HOST}:{PORT}')

def cleanup():
    """Cleanup function"""
    try:
        if os.path.exists("hco_cheatsheet.txt"):
            os.remove("hco_cheatsheet.txt")
    except:
        pass

if __name__ == '__main__':
    # Register cleanup
    import atexit
    atexit.register(cleanup)
    
    # Open browser
    if len(sys.argv) > 1 and sys.argv[1] == '--no-browser':
        print(f"Server starting at http://{HOST}:{PORT}")
    else:
        threading.Thread(target=open_browser).start()
    
    # Start Flask app
    print(f"""
    🚀 HCO Terminal Starting...
    📍 Local: http://{HOST}:{PORT}
    🔧 Press Ctrl+C to stop
    
    Features:
    ✅ Learn Ethical Hacking Path
    ✅ Practice Labs Setup Guides  
    ✅ Tools Installation Check
    ✅ CTF Challenges Resources
    ✅ Downloadable Cheat Sheets
    ✅ Community Links
    
    ⚠️  Educational Use Only - Stay Ethical!
    """)
    
    try:
        app.run(host=HOST, port=PORT, debug=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped. Thank you for using HCO Terminal!")
        cleanup()
