import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")

print("Twilio Settings:")
print(f"SID: {account_sid}")
print(f"Token: {'...' if auth_token else 'None'}")
print(f"From: {from_number}")

if not (account_sid and auth_token and from_number):
    print("Error: Missing Twilio configuration in environment.")
    exit(1)

client = Client(account_sid, auth_token)

to_number = "+9779842756406"
try:
    print(f"Attempting to send SMS to {to_number}...")
    message = client.messages.create(
        body="CareConnect Twilio Integration Test",
        from_=from_number,
        to=to_number
    )
    print(f"SMS Sent successfully! Message SID: {message.sid}")
except Exception as e:
    print(f"Failed to send SMS: {e}")
