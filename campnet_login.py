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
    """Attempts to log into the BITS Goa network."""
    if not USERNAME or not PASSWORD:
        print("Error: CAMPUS_ID or CAMPUS_PASSWORD not found in .env file!")
        return False

    data = {
        "user": USERNAME,
        "password": PASSWORD,
        "cmd": "authenticate",
        "Login": "Login"
    }
    
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Attempting to connect to campnet as {USERNAME}...")
        response = requests.post(PORTAL_URL, data=data, timeout=10, verify=False)
        
        if "Successful" in response.text or response.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] Login successful!")
            return True
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Login failed. Check your ID/Password in .env")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[{time.strftime('%H:%M:%S')}] Portal unreachable (Wi-Fi disconnected?)")
        return False

if __name__ == "__main__":
    print("Campnet Autologin Service Started (Console Mode)...")
    last_status = None 

    while True:
        current_status = is_connected()
        
        if current_status:
            if last_status != True:
                print(f"[{time.strftime('%H:%M:%S')}] Internet connection verified. Standing by...")
            last_status = True
            time.sleep(300) # Check every 5 minutes
        else:
            success = login()
            last_status = success
            # If failed, try again in 10s; if succeeded, wait 5 mins
            time.sleep(300 if success else 10)
