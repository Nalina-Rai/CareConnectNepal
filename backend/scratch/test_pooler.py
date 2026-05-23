import psycopg2
import sys

def test_conn(conn_str):
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        print(f"SUCCESS: {conn_str.split('@')[1]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED: {conn_str.split('@')[1]} - Error: {str(e).strip()}")
        return False

password = "Sujal9842756406"
project_ref = "tjyzribebypemfpmalge"

regions = ["ap-southeast-2", "ap-southeast-1", "ap-south-1", "us-east-1", "us-west-1", "eu-central-1", "eu-west-1"]

for r in regions:
    # Try pooler on port 6543
    conn = f"postgresql://postgres.{project_ref}:{password}@aws-0-{r}.pooler.supabase.com:6543/postgres"
    if test_conn(conn):
        print(f"FOUND WORKING POOLER: {r}")
        break
