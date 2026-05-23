import os
import sys
import django
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careconnect.settings')
django.setup()

from users.models import User, OTP
from rest_framework.test import APIRequestFactory
from users.views import OTPRequestView, OTPVerifyView, RegisterView

factory = APIRequestFactory()

rand = random.randint(1000, 9999)
phone = f"+9779842{rand}"
email = "sujalkunwar22@gmail.com"
password = "TestPassword123!"

print(f"--- SIMULATING REGISTRATION FLOW FOR {email} / {phone} ---")

# Step 1: Request OTP
print("\nStep 1: Requesting OTP...")
request_otp = factory.post('/api/auth/otp/request/', {
    "phone_number": phone,
    "email": email
})
view_otp_req = OTPRequestView.as_view()
response_otp_req = view_otp_req(request_otp)

print(f"OTP Request Response Status: {response_otp_req.status_code}")
if response_otp_req.status_code != 201:
    print(f"OTP Request Failed: {response_otp_req.data}")
    exit(1)

# Retrieve OTP from DB
latest_otp = OTP.objects.filter(phone_number=phone, is_used=False).latest('created_at')
code = latest_otp.code
print(f"Retrieved OTP code from DB: {code}")

# Step 2: Verify OTP
print("\nStep 2: Verifying OTP...")
request_verify = factory.post('/api/auth/otp/verify/', {
    "phone_number": phone,
    "code": code
})
view_verify = OTPVerifyView.as_view()
response_verify = view_verify(request_verify)

print(f"OTP Verify Response Status: {response_verify.status_code}")
if response_verify.status_code != 200:
    print(f"OTP Verification Failed: {response_verify.data}")
    exit(1)
print(f"OTP Verification Success: {response_verify.data}")

# Step 3: Register
print("\nStep 3: Completing User Registration...")
request_register = factory.post('/api/auth/register/', {
    "email": email,
    "phone_number": phone,
    "password": password,
    "role": "user",
    "full_name": "Test Caregiver User",
    "address": "Kathmandu, Nepal",
    "municipality": "Kathmandu",
    "ward": "3"
})
view_register = RegisterView.as_view()
response_register = view_register(request_register)

print(f"Registration Response Status: {response_register.status_code}")
if response_register.status_code != 201:
    print(f"Registration Failed: {response_register.data}")
    exit(1)

print("\n--- REGISTRATION FLOW SUCCESSFUL! ---")
user_data = response_register.data
print(f"Access Token: {user_data.get('access')[:20]}...")
print(f"Registered User Name: {user_data.get('user', {}).get('full_name')}")
print(f"Registered User Username: {user_data.get('user', {}).get('username')}")

# Clean up
User.objects.filter(email=email).delete()
print("\nCleaned up test user successfully.")
