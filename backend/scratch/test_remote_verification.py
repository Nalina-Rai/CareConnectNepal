import requests
import random

api_url = "https://careconnect-snowy.vercel.app/api"
email = "sujal.kunwar@patancollege.edu.np"
rand_suffix = random.randint(1000, 9999)
phone = f"+9779842{rand_suffix}"

print(f"--- TESTING END-TO-END DEPLOYED API FLOW FOR {email} ---")
print(f"Targeting Deployed API: {api_url}")

# Step 1: Request OTP from deployed backend (which now handles SMTP sending)
print("\n[Step 1] Requesting OTP from Vercel Backend...")
try:
    response = requests.post(f"{api_url}/auth/otp/request/", json={
        "phone_number": phone,
        "email": email
    }, timeout=15)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 201:
        print(f"Error: {response.text}")
        exit(1)
    
    data = response.json()
    print(f"Response Data: {data}")
    code = data.get("code")
    bypass_twilio = data.get("bypass_twilio")
    bypass_email = data.get("bypass_email")
    
    print(f"Generated OTP Code: {code}")
    print(f"Bypass Twilio (SMS): {bypass_twilio}")
    print(f"Bypass Email (SMTP): {bypass_email}")
    
except Exception as e:
    print(f"Backend Request Failed: {e}")
    exit(1)

