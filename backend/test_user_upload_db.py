import os
import django
import sys
from django.core.files.uploadedfile import SimpleUploadedFile

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careconnect.settings")
django.setup()

from users.models import User

def test_save_profile():
    # Find a user to test
    user = User.objects.filter(username="sujal@gmail.com").first()
    if not user:
        print("Test user not found.")
        return

    print(f"Before update: profile_image='{user.profile_image}'")

    # Create a dummy image file
    dummy_image = SimpleUploadedFile("test_avatar.png", b"fake image bytes", content_type="image/png")
    
    # Update profile image
    user.profile_image = dummy_image
    user.save()

    # Fetch from db again to verify
    user.refresh_from_db()
    print(f"After update: profile_image='{user.profile_image}'")
    print(f"After update URL: '{user.profile_image.url if user.profile_image else ''}'")

if __name__ == "__main__":
    test_save_profile()
