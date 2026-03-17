"""
Simple database migration script
Run this to add the required columns for lead assignment
"""

import duckdb
from pathlib import Path

# Database path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "database.duckdb"

def migrate():
    print("Starting database migration...")
    
    try:
        # Connect to database
        conn = duckdb.connect(DB_PATH)
        print(f"Connected to database: {DB_PATH}")
        
        # Check current gmail_messages schema
        print("\nCurrent gmail_messages schema:")
        schema = conn.execute("PRAGMA table_info(gmail_messages)").fetchall()
        for col in schema:
            print(f"  {col[1]} {col[2]}")
        
        # Add assigned_to column if it doesn't exist
        try:
            conn.execute("ALTER TABLE gmail_messages ADD COLUMN assigned_to INTEGER")
            print("✓ Added assigned_to column")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("✓ assigned_to column already exists")
            else:
                print(f"Error adding assigned_to: {e}")
        
        # Add assigned_at column if it doesn't exist
        try:
            conn.execute("ALTER TABLE gmail_messages ADD COLUMN assigned_at TIMESTAMP")
            print("✓ Added assigned_at column")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("✓ assigned_at column already exists")
            else:
                print(f"Error adding assigned_at: {e}")
        
        # Check users table
        print("\nCurrent users schema:")
        users_schema = conn.execute("PRAGMA table_info(users)").fetchall()
        for col in users_schema:
            print(f"  {col[1]} {col[2]}")
        
        # Add role column if it doesn't exist
        try:
            conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'manager'")
            print("✓ Added role column to users")
            
            # Update existing users to have manager role
            conn.execute("UPDATE users SET role = 'manager' WHERE role IS NULL OR role = ''")
            print("✓ Updated existing users to manager role")
            
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("✓ role column already exists in users")
            else:
                print(f"Error adding role: {e}")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
        # Test the new columns
        print("\nTesting new columns...")
        test = conn.execute("SELECT COUNT(*) FROM gmail_messages WHERE assigned_to IS NULL").fetchone()
        print(f"Found {test[0]} unassigned leads")
        
        users = conn.execute("SELECT username, role FROM users").fetchall()
        print("Users:")
        for username, role in users:
            print(f"  {username}: {role}")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
