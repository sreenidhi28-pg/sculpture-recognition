
import json
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

with open("backend/sculptures.json", "r", encoding="utf-8") as file:
    sculptures = json.load(file)

try:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            for sculpture in sculptures:
                cur.execute("""
                    INSERT INTO sculptures (
                        object_id, title, artist, classification,
                        medium, object_date, image_url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (object_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        artist = EXCLUDED.artist,
                        classification = EXCLUDED.classification,
                        medium = EXCLUDED.medium,
                        object_date = EXCLUDED.object_date,
                        image_url = EXCLUDED.image_url
                """, (
                    sculpture["object_id"],
                    sculpture.get("title"),
                    sculpture.get("artist"),
                    sculpture.get("classification"),
                    sculpture.get("medium"),
                    sculpture.get("date"),
                    sculpture.get("image_url")
                ))

    print("Sculpture records inserted successfully!")
    print("Total records processed:", len(sculptures))

except Exception as e:
    print("Database error:", e)
