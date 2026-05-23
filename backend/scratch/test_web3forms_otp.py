import os
import requests

access_key = "a345d492-20af-4ecc-8d90-088ea4832774"
recipient_email = "sujalkunwar22@gmail.com"
code = "982143"

print(f"Sending real OTP verification email to {recipient_email} via Web3Forms...")

payload = {
    "access_key": access_key,
    "email": recipient_email,
    "subject": "CareConnect Verification Code (Test)",
    "from_name": "CareConnect Nepal",
    "message": f"Your CareConnect OTP verification code is: {code}. Please enter this code to complete registration.",
}

try:
    response = requests.post("https://api.web3forms.com/submit", json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Failed to submit: {e}")
