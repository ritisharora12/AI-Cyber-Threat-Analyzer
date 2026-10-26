"""
Automated 1-Click Deployment Script for Hugging Face Spaces (24/7 Free Hosting)
Deploys AI Cyber Threat Analyzer directly to Hugging Face Spaces using huggingface_hub.
"""

import os
import sys
import argparse
from huggingface_hub import HfApi, login, whoami

def deploy():
    parser = argparse.ArgumentParser(description="Deploy AI Cyber Threat Analyzer to Hugging Face Spaces (24/7 Free)")
    parser.add_argument("--token", help="Hugging Face Access Token (Write permissions)", default=os.getenv("HF_TOKEN"))
    parser.add_argument("--space-name", help="Name of your Hugging Face Space", default="ai-cyber-threat-analyzer")
    parser.add_argument("--private", action="store_true", help="Make Space private instead of public")
    args = parser.parse_args()

    print("=" * 66)
    print("🚀  AI CYBER THREAT ANALYZER - HUGGING FACE SPACES 24/7 DEPLOYMENT")
    print("=" * 66)

    token = args.token
    if not token:
        print("\nTo deploy 24/7 for FREE to Hugging Face Spaces, you need a free Hugging Face token.")
        print("1. Create/Sign-in to your free account at: https://huggingface.co")
        print("2. Get your free token with 'Write' permissions at: https://huggingface.co/settings/tokens")
        print("   (Click 'Create new token' -> choose 'Write' -> Copy token)\n")
        
        try:
            token = input("Enter your Hugging Face Token (hf_...): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nDeployment cancelled.")
            sys.exit(0)

    if not token or not token.startswith("hf_"):
        print("\n❌ Error: Invalid token. A Hugging Face token begins with 'hf_'")
        sys.exit(1)

    print("\n[*] Authenticating with Hugging Face...")
    try:
        user_info = whoami(token=token)
        username = user_info["name"]
        print(f"[✔] Successfully authenticated as: @{username}")
    except Exception as e:
        print(f"\n❌ Authentication failed: {str(e)}")
        print("Please verify that your token is valid and has 'Write' permissions.")
        sys.exit(1)

    repo_name = args.space_name.lower().replace(" ", "-").replace("_", "-")
    repo_id = f"{username}/{repo_name}"

    print(f"\n[*] Creating / Verifying Hugging Face Space: '{repo_id}' (Docker SDK)...")
    api = HfApi(token=token)
    try:
        api.create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="docker",
            private=args.private,
            exist_ok=True
        )
        print(f"[✔] Space repository ready at: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"\n❌ Failed to create space repository: {str(e)}")
        sys.exit(1)

    print("\n[*] Packaging and uploading project files to Hugging Face...")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    ignore_patterns = [
        ".git*",
        "__pycache__*",
        "*.pyc",
        ".env",
        ".pytest_cache*",
        "*.log",
        ".gemini*"
    ]

    try:
        api.upload_folder(
            folder_path=current_dir,
            repo_id=repo_id,
            repo_type="space",
            ignore_patterns=ignore_patterns,
            commit_message="Deploy AI Cyber Threat Analyzer to 24/7 Docker Space"
        )
        print("[✔] Upload completed successfully!")
    except Exception as e:
        print(f"\n❌ File upload failed: {str(e)}")
        sys.exit(1)

    # Hugging Face Direct App Subdomain
    # e.g., username-repo-name.hf.space
    subdomain = f"{username.lower()}-{repo_name.lower()}".replace("_", "-")
    direct_app_url = f"https://{subdomain}.hf.space"
    space_page_url = f"https://huggingface.co/spaces/{repo_id}"

    print("\n" + "=" * 66)
    print("🎉  DEPLOYMENT SUCCESSFUL! YOUR APP IS NOW RUNNING 24/7 IN THE CLOUD")
    print("=" * 66)
    print(f"🌐 Space Dashboard:  {space_page_url}")
    print(f"📱 Live 24/7 Web URL: {direct_app_url}")
    print("=" * 66)
    print("\n📌 What happens next:")
    print("1. Hugging Face is currently building your Docker container (~1-2 minutes).")
    print("2. Once building completes, your site will be live 24/7 at the link above.")
    print("3. You can access it on ANY Android phone, iPhone, iPad, or computer worldwide,")
    print("   and it will STAY ONLINE PERMANENTLY, EVEN WHEN YOUR LAPTOP IS OFF!")
    print("=" * 66 + "\n")

if __name__ == "__main__":
    deploy()
