import requests
import time
import urllib3
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Hides the "Unverified HTTPS request" warning in your logs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- SECURE CREDENTIALS ---
USERNAME = os.getenv("CAMPUS_ID")
PASSWORD = os.getenv("CAMPUS_PASSWORD")
# ------------------------

# The 8090 portal handles authentication at the same URL via POST
PORTAL_URL = "https://campnet.bits-goa.ac.in:8090/httpclient.html"
CHECK_URL = "http://connectivitycheck.gstatic.com/generate_204"

def is_connected():
    """Checks if we already have internet access."""
    try:
        response = requests.get(CHECK_URL, timeout=5)
        return response.status_code == 204
    except:
        return False

def login():
    """Attempts to log into the Cyberoam/Sophos portal."""
    if not USERNAME or not PASSWORD:
        print(f"[{time.strftime('%H:%M:%S')}] Error: Credentials missing in .env")
        return False

    # Cyberoam/Sophos 8090 specific payload
    # 'mode': 191 tells the server this is a LOGIN attempt
    data = {
        "mode": "191",
        "username": USERNAME,
        "password": PASSWORD,
        "a": int(time.time() * 1000), # Some portals require a timestamp
        "producttype": "0"
    }
    
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Attempting 8090 login for {USERNAME}...")
        
        response = requests.post(
            PORTAL_URL, 
            data=data, 
            timeout=10, 
            verify=False,
            proxies={'http': None, 'https': None}
        )
        
        # Cyberoam returns an XML response usually containing <message>
        if "Successful" in response.text or "status=\"login\"" in response.text:
            print(f"[{time.strftime('%H:%M:%S')}] Login successful!")
            return True
        elif "maximum login limit" in response.text:
            print(f"[{time.strftime('%H:%M:%S')}] Already logged in elsewhere.")
            return True
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Login failed. Check your credentials.")
            return False
            
    except requests.exceptions.RequestException:
        print(f"[{time.strftime('%H:%M:%S')}] Portal unreachable. Check Wi-Fi connection.")
        return False

if __name__ == "__main__":
    print("--- BITS Goa 8090 Autologin ---")
    last_status = None 

    while True:
        current_status = is_connected()
        
        if current_status:
            if last_status != True:
                print(f"[{time.strftime('%H:%M:%S')}] Online. Standing by...")
            last_status = True
            time.sleep(300) 
        else:
            success = login()
            last_status = success
            time.sleep(300 if success else 10)
