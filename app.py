"""
AI Cyber Threat Analyzer - Main Application Server.
Provides modern REST API endpoints for phishing message detection,
URL extraction & threat scanning, file malware analysis, and explainable AI insights.
"""

import os
import sys
import time
import tempfile
import uuid
import socket
import io

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

import qrcode
import qrcode.image.svg
from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from threat_engine.threat_intel import ThreatIntelManager
from threat_engine.url_scanner import URLScanner
from threat_engine.message_scanner import MessageScanner
from threat_engine.file_scanner import FileScanner
from threat_engine.ai_explainer import AIExplainer

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
# Allow file uploads up to 250MB for scanning various file sizes
app.config["MAX_CONTENT_LENGTH"] = 250 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.path.join(tempfile.gettempdir(), "ai_cybershield_uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize engines
gemini_key = os.getenv("GEMINI_API_KEY", "")
abuse_key = os.getenv("ABUSE_CH_KEY", "")

intel_manager = ThreatIntelManager(abuse_ch_key=abuse_key)
url_scanner = URLScanner(intel_manager=intel_manager)
message_scanner = MessageScanner(url_scanner=url_scanner)
file_scanner = FileScanner(intel_manager=intel_manager)
ai_explainer = AIExplainer(gemini_api_key=gemini_key)

SAMPLE_MAP = {
    "phishing_paypal": {
        "title": "PayPal Security Alert Phishing",
        "category": "Message",
        "file": "test_samples/phishing_paypal.txt"
    },
    "ceo_fraud": {
        "title": "CEO Business Email Compromise (BEC)",
        "category": "Message",
        "file": "test_samples/ceo_fraud.txt"
    },
    "fake_invoice": {
        "title": "Overdue Invoice Scam with Raw IP Link",
        "category": "Message",
        "file": "test_samples/fake_invoice.txt"
    },
    "clean_email": {
        "title": "Legitimate Corporate Team Sync",
        "category": "Message",
        "file": "test_samples/clean_email.txt"
    },
    "suspicious_script": {
        "title": "PowerShell In-Memory Download Cradle",
        "category": "File",
        "file": "test_samples/suspicious_script.ps1"
    },
    "ransomware_note": {
        "title": "Ransomware Extortion Note",
        "category": "File",
        "file": "test_samples/ransomware_simulation_note.txt"
    }
}


def get_local_ip():
    """Discovers the machine's local IPv4 address on the Wi-Fi/LAN."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


@app.route("/")
def index():
    """Renders the main Cyber Threat Analyzer dashboard."""
    return render_template("index.html")


@app.route("/manifest.json")
def pwa_manifest():
    """Serves PWA manifest for Android and iOS Add to Home Screen."""
    return jsonify({
        "name": "AI Cyber Threat Analyzer",
        "short_name": "CyberShield",
        "description": "Autonomous Phishing, URL & Malware Security Intelligence",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#070a13",
        "theme_color": "#070a13",
        "icons": [
            {
                "src": "/static/icons/icon.svg",
                "sizes": "any",
                "type": "image/svg+xml"
            }
        ]
    })


@app.route("/api/network-info")
def network_info():
    """Returns local LAN IP, port, and mobile URL for phone pairing."""
    port = int(os.environ.get("PORT", 5000))
    local_ip = get_local_ip()
    return jsonify({
        "local_ip": local_ip,
        "port": port,
        "desktop_url": f"http://localhost:{port}",
        "mobile_url": f"http://{local_ip}:{port}"
    })


@app.route("/api/qrcode")
def generate_qrcode():
    """Generates an SVG QR code pointing to the mobile access URL."""
    port = int(os.environ.get("PORT", 5000))
    local_ip = get_local_ip()
    mobile_url = f"http://{local_ip}:{port}"

    factory = qrcode.image.svg.SvgPathImage
    qr_img = qrcode.make(mobile_url, image_factory=factory, box_size=10, border=2)
    buf = io.BytesIO()
    qr_img.save(buf)
    svg_data = buf.getvalue()

    return Response(svg_data, mimetype="image/svg+xml")



@app.route("/api/config", methods=["GET", "POST"])
def manage_config():
    """Gets or updates analyzer configuration and AI keys."""
    global gemini_key, abuse_key, intel_manager, url_scanner, message_scanner, file_scanner, ai_explainer

    if request.method == "POST":
        data = request.get_json() or {}
        new_gemini = data.get("gemini_api_key", "").strip()
        new_abuse = data.get("abuse_ch_key", "").strip()

        if "gemini_api_key" in data:
            gemini_key = new_gemini
            ai_explainer.gemini_api_key = gemini_key

        if "abuse_ch_key" in data:
            abuse_key = new_abuse
            intel_manager.abuse_ch_key = abuse_key

        # Save to local .env for persistence
        try:
            with open(".env", "w") as f:
                if gemini_key:
                    f.write(f"GEMINI_API_KEY={gemini_key}\n")
                if abuse_key:
                    f.write(f"ABUSE_CH_KEY={abuse_key}\n")
        except Exception:
            pass

        return jsonify({
            "status": "success",
            "message": "Configuration updated successfully",
            "gemini_active": bool(gemini_key),
            "abuse_active": bool(abuse_key)
        })

    return jsonify({
        "gemini_configured": bool(gemini_key),
        "abuse_ch_configured": bool(abuse_key),
        "threat_intel_sources": [
            {"name": "Cloudflare Security DoH (1.1.1.2)", "type": "Malware & Phishing DNS", "free": True, "status": "Active"},
            {"name": "Google Public DNS JSON API", "type": "A/MX/SPF Resolution", "free": True, "status": "Active"},
            {"name": "RDAP Registration Authority", "type": "Domain Age & Registrar", "free": True, "status": "Active"},
            {"name": "IP-API Geolocation & ASN", "type": "Hosting & IP Reputation", "free": True, "status": "Active"},
            {"name": "Local Heuristic Neural Engine", "type": "Zero-latency NLP & Signatures", "free": True, "status": "Active"},
            {"name": "Google Gemini Free AI (Optional)", "type": "LLM Deep Incident Response", "free": True, "status": "Configured" if gemini_key else "Ready (Free key can be added)"}
        ]
    })


@app.route("/api/sample/<sample_id>", methods=["GET"])
def get_sample(sample_id):
    """Retrieves preset test samples for rapid testing."""
    if sample_id not in SAMPLE_MAP:
        return jsonify({"error": "Sample not found"}), 404

    meta = SAMPLE_MAP[sample_id]
    try:
        with open(meta["file"], "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({
            "id": sample_id,
            "title": meta["title"],
            "category": meta["category"],
            "content": content
        })
    except Exception as e:
        return jsonify({"error": f"Failed to load sample: {str(e)}"}), 500


@app.route("/api/scan/message", methods=["POST"])
def scan_message_endpoint():
    """
    Scans a message or email for phishing indicators, extracts all URLs,
    and returns risk score, warning signs breakdown, and safety recommendations.
    """
    t0 = time.time()
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Message text cannot be empty."}), 400

    # Scan message and extract URLs
    scan_res = message_scanner.scan(text)

    # Build report with AI explanation
    duration_ms = (time.time() - t0) * 1000
    report = ai_explainer.build_report(
        scan_type="message",
        risk_score=scan_res["risk_score"],
        indicators=scan_res["indicators"],
        extracted_urls=scan_res["extracted_urls"],
        duration_ms=duration_ms
    )

    return jsonify(report.to_dict())


@app.route("/api/scan/url", methods=["POST"])
def scan_url_endpoint():
    """
    Scans a single URL for malicious indicators, brand spoofing,
    homoglyphs, IP hostnames, and live threat intelligence.
    """
    t0 = time.time()
    data = request.get_json() or {}
    raw_url = data.get("url", "").strip()

    if not raw_url:
        return jsonify({"error": "URL cannot be empty."}), 400

    url_res = url_scanner.scan_url(raw_url)

    duration_ms = (time.time() - t0) * 1000
    report = ai_explainer.build_report(
        scan_type="url",
        risk_score=url_res.risk_score,
        indicators=url_res.indicators,
        extracted_urls=[url_res.to_dict()],
        duration_ms=duration_ms
    )

    return jsonify(report.to_dict())


@app.route("/api/scan/file", methods=["POST"])
def scan_file_endpoint():
    """
    Handles file upload of various sizes (small scripts, documents, large files)
    to check for viruses, packers, entropy anomalies, and malicious heuristics.
    """
    t0 = time.time()
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    original_filename = secure_filename(uploaded_file.filename) or "sample.bin"
    temp_filename = f"{uuid.uuid4().hex}_{original_filename}"
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], temp_filename)

    try:
        # Save file to temp path
        uploaded_file.save(temp_path)

        # Run multi-tier file scanner
        file_res = file_scanner.scan_file(temp_path, original_filename)

        duration_ms = (time.time() - t0) * 1000
        report = ai_explainer.build_report(
            scan_type="file",
            risk_score=file_res["risk_score"],
            indicators=file_res["indicators"],
            file_info=file_res,
            duration_ms=duration_ms
        )

        return jsonify(report.to_dict())

    except Exception as e:
        return jsonify({"error": f"Error scanning file: {str(e)}"}), 500

    finally:
        # Clean up temporary upload file safely
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


@app.route("/api/report/export", methods=["POST"])
def export_report_endpoint():
    """Exports the threat report as formatted Markdown or JSON."""
    data = request.get_json() or {}
    report = data.get("report", {})
    fmt = data.get("format", "markdown").lower()

    if fmt == "json":
        import json
        return jsonify({"content": json.dumps(report, indent=2), "mime": "application/json"})

    # Markdown export
    lines = [
        f"# Cyber Threat Intelligence Incident Report",
        f"**Report ID**: `{report.get('scan_id', 'N/A')}`",
        f"**Scan Type**: {report.get('scan_type', '').upper()}",
        f"**Risk Score**: **{report.get('risk_score', 0)}/100** ({report.get('threat_level', 'UNKNOWN')})",
        f"**AI Engine**: {report.get('ai_engine_used', 'Local AI Engine')}",
        "",
        "## Executive Summary",
        report.get("executive_summary", "No summary provided."),
        "",
        "## Detailed Threat Analysis & Warning Signs",
        report.get("detailed_explanation", "No indicators flagged."),
        "",
        "## Actionable Safety Recommendations"
    ]

    for rec in report.get("recommendations", []):
        lines.append(f"- **[{rec.get('priority')}] {rec.get('action')}**: {rec.get('detail')}")

    if report.get("mitre_attack"):
        lines.append("")
        lines.append("## MITRE ATT&CK Matrix Alignment")
        for m in report.get("mitre_attack", []):
            lines.append(f"- `{m.get('id')}`: {m.get('name')}")

    if report.get("file_info"):
        f = report["file_info"]
        lines.append("")
        lines.append("## File Metadata & Hashes")
        lines.append(f"- **Filename**: `{f.get('filename')}`")
        lines.append(f"- **Size**: {f.get('size_formatted')}")
        lines.append(f"- **SHA-256**: `{f.get('sha256')}`")
        lines.append(f"- **MD5**: `{f.get('md5')}`")
        lines.append(f"- **MIME Type**: `{f.get('mime_type')}` ({f.get('magic_desc')})")
        lines.append(f"- **Shannon Entropy**: `{f.get('entropy')}` / 8.0")

    md_content = "\n".join(lines)
    return jsonify({"content": md_content, "mime": "text/markdown"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    local_ip = get_local_ip()
    print("=" * 64)
    print("[*] AI CYBER THREAT ANALYZER (CYBERSHIELD) IS RUNNING")
    print("=" * 64)
    print(f"[*] Localhost Desktop Access:     http://localhost:{port}")
    print(f"[*] Mobile Device (Android/iOS):  http://{local_ip}:{port}")
    print(f"[*] (Ensure mobile phone is on the same Wi-Fi network)")
    print("=" * 64)
    app.run(host="0.0.0.0", port=port, debug=False)
