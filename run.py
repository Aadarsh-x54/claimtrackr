"""
ClaimTrackr - Application Launcher
Runs the Flask application with pre-flight environment checks.
"""

import os
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("=" * 60)
    print(" ClaimTrackr: AI-Powered Insurance Claim Automation System")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR KEY HERE" or api_key == "your_openai_api_key_here":
        print("[!] Warning: OPENAI_API_KEY is not set or using placeholder.")
        print("    Please add your valid OpenAI key to the .env file.")
        print("    Example: OPENAI_API_KEY=sk-proj-...")
        print("-" * 60)
    else:
        print("[✓] OpenAI API Key detected.")
    
    port = int(os.getenv("PORT", 8081))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"[*] Starting server at http://localhost:{port} ...")
    print("=" * 60)
    
    try:
        from main_BUPA import app
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        print(f"[X] Failed to launch server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
