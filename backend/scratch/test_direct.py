import psycopg2

try:
    conn = psycopg2.connect("postgresql://postgres:Sujal9842756406@db.tjyzribebypemfpmalge.supabase.co:5432/postgres")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("DIRECT CONNECTION SUCCESSFUL!")
    cur.close()
    conn.close()
except Exception as e:
    print(f"DIRECT CONNECTION FAILED: {e}")
