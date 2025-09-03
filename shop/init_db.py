# init_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db.sqlite3"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Create tables if they don't exist ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    created_at TEXT,
    updated_at TEXT
)
""")

# --- Ensure `is_admin` column exists in users ---
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]
if "is_admin" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0")
    print("🛠️ Added 'is_admin' column to users table.")

# --- Insert admin user (plaintext password) ---
cursor.execute("SELECT * FROM users WHERE email = ?", ("admin@example.com",))
if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
        ("admin@example.com", "admin123", 1)  # plain text
    )
    print("✅ Admin user created: admin@example.com / admin123")
else:
    cursor.execute("UPDATE users SET is_admin = 1 WHERE email = ?", ("admin@example.com",))

# --- Insert sample products ---
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute(
        "INSERT INTO products (name, description, price, stock, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))",
        ("Laptop", "A powerful laptop", 1200.0, 10)
    )
    cursor.execute(
        "INSERT INTO products (name, description, price, stock, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))",
        ("Phone", "A smart phone", 800.0, 25)
    )
    print("✅ Sample products added.")

conn.commit()
conn.close()
print("🎉 Database initialized successfully (⚠️ passwords stored in plain text).")
