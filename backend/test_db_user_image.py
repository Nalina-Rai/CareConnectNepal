import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careconnect.settings")
django.setup()

from users.models import User

def print_user_images():
    print("--- USER PROFILE IMAGES IN DATABASE ---")
    users = User.objects.all()
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}, Full Name: {u.full_name}, Profile Image (field): '{u.profile_image}', Name: '{u.profile_image.name if u.profile_image else ''}', URL: '{u.profile_image.url if u.profile_image else ''}'")

if __name__ == "__main__":
    print_user_images()
