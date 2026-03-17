import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "database.duckdb"

conn = duckdb.connect(DB_PATH)

# Check if role column exists
try:
    conn.execute("SELECT role FROM users LIMIT 1")
    print("Column 'role' already exists")
except:
    print("Adding 'role' column...")
    conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'manager'")
    print("Column added")

# Update admin role
conn.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
print("Admin role set to 'admin'")

# Delete duplicate admin
conn.execute("DELETE FROM users WHERE id = 5")
print("Duplicate admin deleted")

# Show all users
rows = conn.execute("SELECT id, username, email, role FROM users").fetchall()
print("\nAll users:")
for r in rows:
    print(f"  {r}")

conn.close()
print("\nDone!")
