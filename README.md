---
title: AI Cyber Threat Analyzer
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🛡️ AI Cyber Threat Analyzer (Cybershield)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deploy%20Ready-46E3B7.svg)](https://render.com/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces%20Ready-FFD21E.svg)](https://huggingface.co/spaces)

> **Autonomous Cyber Threat Intelligence & Phishing Defense Engine**  
> Detects phishing indicators, extracts & scans URLs, inspects file uploads of various sizes for viruses, explains warning signs using AI, and computes real-time risk scores with tailored safety recommendations — powered entirely by **100% free AI tools and resources**.

---

## 🌟 Key Capabilities

### 1. 💬 Phishing & Social Engineering Detection
- **Psychological Urgency & Fear Exploitation**: Flags deadlines under 24 hours, threats of account termination, legal intimidation, and fake security alarms.
- **Credential Harvesting Directives**: Detects lures steering victims to submit passwords, verify billing information, or update MFA details.
- **Business Email Compromise (BEC)**: Detects CEO impersonation, emergency wire transfer requests, and gift card fraud patterns.
- **Obfuscation Detection**: Identifies zero-width space evasion and defanged indicators (`hxxps[:]//`).

### 2. 🔗 Automatic URL Extraction & Threat Deep Scan
- **Automatic Link Extraction**: Extracts standard links, bare domains, and defanged URLs (`hxxp://`, `example[.]com`) automatically from raw message text.
- **IDN Homoglyph & Punycode Detection**: Detects Cyrillic and Greek lookalike characters designed to mimic legitimate domains (e.g. Cyrillic `а` in `pаypal-security-update.xyz`).
- **Deceptive Brand Hijacking**: Detects brand names (`paypal`, `microsoft`, `apple`, `google`, `netflix`) placed in subdomains or paths on unauthorized hosts.
- **Direct IP Hostnames & Risky TLDs**: Flags URLs hosted on raw IP addresses (`http://185.220...`) and high-risk top-level domains (`.zip`, `.mov`, `.top`, `.xyz`, `.buzz`, `.tk`).
- **Live Cloudflare Security DoH (1.1.1.2)**: Automatically verifies if a domain is blocked by Cloudflare's global malware and phishing threat intelligence network.

### 3. 📁 Multi-Size File Malware & Virus Inspection (Python + C)
- **Streaming Chunked Hashing**: Computes **MD5, SHA-1, and SHA-256** in constant $O(1)$ memory chunks, allowing seamless uploads of small scripts up to 250MB+ archives without memory spikes.
- **C-Accelerated Entropy Engine**: Includes native C module (`threat_engine/c_threat_core.c`) for ultra-fast Shannon entropy computation across large files (with graceful Python fallback).
- **Magic Byte Masquerading**: Verifies actual binary headers against file extensions (e.g., flagging Windows PE executables disguised as `.pdf` or `.png`).
- **Shannon Byte Entropy Gauge**: Calculates byte entropy (0.0 to 8.0) across the file to detect UPX-packed payloads and encrypted ransomware.
- **Static Heuristic Inspection**: Scans for PowerShell in-memory download cradles (`IEX Net.WebClient`), reverse shell patterns, dangerous Win32 memory injection APIs (`VirtualAllocEx`, `WriteProcessMemory`), Office VBA macros, and ransomware extortion notes.

### 4. 🧠 Explainable AI Security Reasoning & MITRE ATT&CK Mapping
- **Explainable Warning Signs**: Breaks down *why* each indicator was flagged, providing technical evidence, the attacker's motive, and risk contribution.
- **MITRE ATT&CK Alignment**: Automatically maps detected techniques to MITRE IDs (`T1566` Phishing, `T1059` Command Execution, `T1036` Masquerading, `T1027` Obfuscation).
- **Dual AI Mode**:
  - **Local Heuristic Neural Model (Default)**: 100% free, runs offline, instantaneous ($<5\text{ ms}$), zero tokens or keys required.
  - **Google Gemini 1.5/2.0 Flash (Free Tier)**: Option to enter a free API key from [Google AI Studio](https://aistudio.google.com/) for natural, conversational Tier-3 SOC analyst reports.

### 5. 📱 Android & iOS Mobile Device Support
- **1-Tap Clipboard Paste**: Instant scan for suspicious SMS, WhatsApp, or Telegram messages.
- **Native Mobile Share Sheet**: Share incident threat reports directly to WhatsApp, Slack, Notes, or Messages.
- **PWA "Add to Home Screen"**: Installable on Android (Chrome) and iOS (Safari) as a fullscreen app.
- **Instant QR Code Scanner**: Scan the desktop QR code with your phone camera to pair instantly.

---

## 🆓 100% Free Threat Intelligence Stack Used

| Resource | Role | Cost / Tier |
|---|---|---|
| **Local Cyber Defense Engine** | Rule-based NLP, magic bytes, entropy, static signatures | **100% Free & Offline** |
| **C Threat Core (`c_threat_core.c`)** | Fast C-level entropy & signature pattern searching | **100% Free & Open Source** |
| **Cloudflare Security DoH (`1.1.1.2`)** | Live phishing and malware domain blocking verification | **100% Free Public API** |
| **Google Public DNS Engine** | Authoritative A, MX, and SPF resolution | **100% Free Public API** |
| **RDAP Protocol (`rdap.org`)** | Domain creation date and registrar age verification | **100% Free Public Protocol** |
| **IP-API** | Host geolocation, ASN, and hosting provider reputation | **100% Free Public API** |
| **Google Gemini 1.5/2.0 Flash** *(Optional)* | Generative Tier-3 SOC incident response briefing | **Free Tier (Google AI Studio)** |

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.11, 3.12, 3.14)
- (Optional) GCC for compiling C acceleration module

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-cyber-threat-analyzer.git
cd ai-cyber-threat-analyzer

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
*(On Windows, you can simply double-click `run_cybershield.bat`)*

Open your browser and navigate to:
```
http://localhost:5000
```

---

## ☁️ 1-Click Free Cloud Deployment (24/7 Hosting)

### Option A: Deploy on Render.com (100% Free)
1. Fork or push this repository to your GitHub account.
2. Go to [dashboard.render.com](https://dashboard.render.com) and click **New +** $\to$ **Web Service**.
3. Connect your repository.
4. Set:
   - **Environment**: `Python 3`
   - **Build Command**: `gcc -O3 -shared -fPIC -o threat_engine/c_threat_core.so threat_engine/c_threat_core.c 2>/dev/null || true; pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: `Free`
5. Click **Create Web Service**. Your app is live 24/7!

### Option B: Deploy on Hugging Face Spaces (100% Free)
1. Create a free Space at [huggingface.co/new-space](https://huggingface.co/new-space) (choose **Docker**).
2. Upload these repository files.
3. Hugging Face will automatically build the container and provide a 24/7 HTTPS URL!  
*(Or run `python deploy_to_huggingface.py` locally to deploy in 1 click)*

---

## 🧪 Built-in Test Attack Presets

The analyzer includes ready-to-test attack simulations in `test_samples/`:

| Sample Preset | Attack Vector Simulated | Expected Verdict |
|---|---|---|
| **PayPal Phish** | Brand impersonation + artificial urgency + homoglyph link | ⛔ CRITICAL THREAT (100/100) |
| **CEO Fraud** | Business Email Compromise with confidential wire transfer | ⛔ CRITICAL THREAT (100/100) |
| **Fake Invoice** | Coercive legal threat + raw IP hosting link | ⛔ CRITICAL THREAT (100/100) |
| **PowerShell Script** | In-memory download cradle with `-WindowStyle Hidden` | ⚠️ SUSPICIOUS (55/100) |
| **Ransomware Note** | Extortion note with Bitcoin address and countdown | ⚠️ SUSPICIOUS / HIGH |
| **Clean Corporate Email**| Standard corporate meeting sync with official documentation link | ✅ SAFE (0/100) |

---

## 📁 Repository Directory Structure

```
ai-cyber-threat-analyzer/
├── app.py                      # Flask REST API and web controller
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Production container definition (Python + GCC)
├── Procfile                    # Cloud web process entry point
├── render.yaml                 # Render.com 1-click blueprint
├── deploy_to_huggingface.py    # Automated Hugging Face deployer
├── deploy_to_huggingface.bat   # Windows 1-click Hugging Face launcher
├── run_cybershield.bat         # Windows 1-click local launcher
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── .env.example                # Example environment variables
├── README.md                   # Complete system documentation
├── threat_engine/              # Core threat intelligence & analysis engine
│   ├── __init__.py
│   ├── models.py               # Data models for indicators, reports, and URLs
│   ├── threat_intel.py         # Free Threat Intel Manager (Cloudflare DoH, RDAP, DNS)
│   ├── url_scanner.py          # URL extraction, homoglyph detection, brand spoofing
│   ├── message_scanner.py      # Phishing NLP, urgency detection, BEC fraud
│   ├── file_scanner.py         # Multi-size streaming hash, magic bytes, entropy
│   ├── ai_explainer.py         # Explainable AI engine (Local + Gemini Hybrid)
│   └── c_threat_core.c         # C module for high-speed entropy computation
├── templates/
│   └── index.html              # Cyber Operations Center dashboard UI
├── static/
│   ├── css/
│   │   └── styles.css          # Cyber-grade dark theme, glowing meters
│   ├── js/
│   │   └── app.js              # Real-time UI logic, SVG gauge animator
│   └── icons/
│       └── icon.svg            # PWA high-res vector application icon
└── test_samples/               # Calibrated attack samples for testing
    ├── clean_email.txt
    ├── phishing_paypal.txt
    ├── ceo_fraud.txt
    ├── fake_invoice.txt
    ├── suspicious_script.ps1
    └── ransomware_simulation_note.txt
```

---

## 📄 Incident Report Export
Every scan can be exported with one click into:
- **Markdown Report (`.md`)**: Full SOC incident brief ready for sharing with security teams or archiving.
- **Raw JSON**: Structured machine-readable incident data including all indicators, confidence metrics, and hashes.

---

## 🛡️ License
Released under the [MIT License](LICENSE). Free for personal, educational, and commercial use.
