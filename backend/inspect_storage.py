import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careconnect.settings")
django.setup()

from django.db import connection

def inspect_storage():
    with connection.cursor() as cursor:
        # Check buckets
        try:
            cursor.execute("SELECT id, name, public, file_size_limit, allowed_mime_types FROM storage.buckets;")
            buckets = cursor.fetchall()
            print("--- BUCKETS ---")
            for b in buckets:
                print(f"ID: {b[0]}, Name: {b[1]}, Public: {b[2]}, Limit: {b[3]}, Types: {b[4]}")
        except Exception as e:
            print("Error reading buckets:", e)

        # Check policies on storage.objects
        try:
            cursor.execute("""
                SELECT policyname, cmd, qual, with_check 
                FROM pg_policies 
                WHERE tablename = 'objects' AND schemaname = 'storage';
            """)
            policies = cursor.fetchall()
            print("\n--- POLICIES ON storage.objects ---")
            for p in policies:
                print(f"Policy: {p[0]}, Command: {p[1]}, Qual: {p[2]}, With Check: {p[3]}")
        except Exception as e:
            print("Error reading policies:", e)

if __name__ == "__main__":
    inspect_storage()
