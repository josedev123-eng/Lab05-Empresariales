import sqlite3
import os

base = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base, 'db.sqlite3')

conn = sqlite3.connect(db_path)
c = conn.cursor()

print("=== Tables ===")
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in c.fetchall():
    print(f"  {row[0]}")

print("\n=== quiz_exam columns ===")
c.execute("PRAGMA table_info(quiz_exam)")
for row in c.fetchall():
    print(f"  {row}")

print("\n=== quiz_question columns ===")
c.execute("PRAGMA table_info(quiz_question)")
for row in c.fetchall():
    print(f"  {row}")

print("\n=== quiz_choice columns ===")
c.execute("PRAGMA table_info(quiz_choice)")
for row in c.fetchall():
    print(f"  {row}")

conn.close()