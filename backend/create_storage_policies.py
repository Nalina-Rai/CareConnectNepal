import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careconnect.settings")
django.setup()

from django.db import connection

def create_policies():
    sql_commands = [
        # Drop existing policies to start clean or avoid conflicts
        "DROP POLICY IF EXISTS \"Allow public read access\" ON storage.objects;",
        "DROP POLICY IF EXISTS \"Allow public insert access\" ON storage.objects;",
        "DROP POLICY IF EXISTS \"Allow public update access\" ON storage.objects;",
        "DROP POLICY IF EXISTS \"Allow public delete access\" ON storage.objects;",
        
        # Create policies
        "CREATE POLICY \"Allow public read access\" ON storage.objects FOR SELECT TO public USING (true);",
        "CREATE POLICY \"Allow public insert access\" ON storage.objects FOR INSERT TO public WITH CHECK (true);",
        "CREATE POLICY \"Allow public update access\" ON storage.objects FOR UPDATE TO public USING (true) WITH CHECK (true);",
        "CREATE POLICY \"Allow public delete access\" ON storage.objects FOR DELETE TO public USING (true);"
    ]
    
    with connection.cursor() as cursor:
        for cmd in sql_commands:
            try:
                cursor.execute(cmd)
                print(f"Executed: {cmd}")
            except Exception as e:
                print(f"Error executing '{cmd}': {e}")

if __name__ == "__main__":
    create_policies()
