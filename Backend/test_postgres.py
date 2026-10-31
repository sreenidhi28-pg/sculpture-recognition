
import psycopg

DATABASE_URL = "postgresql://postgres:sculpture123@localhost:5432/sculpture_db"

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:

        cur.execute("SELECT COUNT(*) FROM sculptures")
        total = cur.fetchone()[0]

        print("Total sculptures in PostgreSQL:", total)

        cur.execute("""
            SELECT object_id, title, artist, medium
            FROM sculptures
            LIMIT 5
        """)

        print("\n--- SAMPLE SCULPTURE RECORDS ---")

        for row in cur.fetchall():
            print(row)
