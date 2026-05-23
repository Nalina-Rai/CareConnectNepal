import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careconnect.settings")
django.setup()

from django.conf import settings
from core.supabase import upload_to_supabase

print("SUPABASE_URL:", settings.SUPABASE_URL)
print("SUPABASE_ANON_KEY:", settings.SUPABASE_ANON_KEY[:10] + "..." if settings.SUPABASE_ANON_KEY else "None")

# Test upload with dummy text file
dummy_data = b"Hello from CareConnect test file"
url = upload_to_supabase(dummy_data, "profiles", "test_file.txt", "text/plain")
print("Upload result URL:", url)
