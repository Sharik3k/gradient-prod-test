"""
Script to migrate the existing database to support lead assignment
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import conn

def migrate_database():
    print("Migrating database schema...")
    
    try:
        # Check if role column exists in users table
        check_role = conn.execute("""
            SELECT COUNT(*) as count FROM pragma_table_info('users') WHERE name = 'role'
        """).fetchone()
        
        if check_role[0] == 0:
            print("Adding 'role' column to users table...")
            conn.execute("""
                ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'manager'
            """)
            
            # Add check constraint
            conn.execute("""
                ALTER TABLE users ADD CONSTRAINT check_role CHECK (role IN ('admin', 'manager'))
            """)
            
            # Update existing users to be managers by default
            conn.execute("""
                UPDATE users SET role = 'manager' WHERE role IS NULL OR role = ''
            """)
            
            print("✓ Added role column to users table")
        else:
            print("✓ Role column already exists in users table")
        
        # Check if assigned_to column exists in gmail_messages table
        check_assigned_to = conn.execute("""
            SELECT COUNT(*) as count FROM pragma_table_info('gmail_messages') WHERE name = 'assigned_to'
        """).fetchone()
        
        if check_assigned_to[0] == 0:
            print("Adding lead assignment columns to gmail_messages table...")
            conn.execute("""
                ALTER TABLE gmail_messages ADD COLUMN assigned_to INTEGER
            """)
            conn.execute("""
                ALTER TABLE gmail_messages ADD COLUMN assigned_at TIMESTAMP
            """)
            print("✓ Added assignment columns to gmail_messages table")
        else:
            print("✓ Assignment columns already exist in gmail_messages table")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        # Show current schema
        print("\nCurrent users table schema:")
        users_schema = conn.execute("PRAGMA table_info(users)").fetchall()
        for col in users_schema:
            print(f"  {col[1]} {col[2]} {'NOT NULL' if col[3] else ''} {'DEFAULT ' + str(col[4]) if col[4] is not None else ''}")
        
        print("\nCurrent gmail_messages table schema (relevant columns):")
        messages_schema = conn.execute("PRAGMA table_info(gmail_messages)").fetchall()
        for col in messages_schema:
            if col[1] in ['gmail_id', 'assigned_to', 'assigned_at', 'created_at']:
                print(f"  {col[1]} {col[2]} {'NOT NULL' if col[3] else ''} {'DEFAULT ' + str(col[4]) if col[4] is not None else ''}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise

if __name__ == "__main__":
    migrate_database()
