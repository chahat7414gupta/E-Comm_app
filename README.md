# 🛒 Django + SQLAlchemy + Jinja (SQLite) — E-Commerce CRUD App  

A minimal full-stack assignment project for an **e-commerce platform** built with:  
- **Django** → Routing, auth/session, static files  
- **SQLAlchemy** → ORM for Users & Products (SQLite backend)  
- **Jinja2** → Clean, reusable templates (dark-mode styled)  

---

## ✨ Features  
- 🔑 **User Authentication**  
  - Register with email + password (hashed with PBKDF2)  
  - Login / Logout (session-based)  
- 👀 **Product Browsing**  
  - All users can view products  
- 🛠️ **Admin Controls**  
  - Create / Edit / Delete products  
  - Extra `is_admin` flag on Users for access control  
- 🧩 **UI/UX**  
  - Jinja2 templates styled in **dark mode**  
  - Responsive product grid with modern cards  
  - Clear login/register/product forms  

---

## 🚀 Quickstart  

```bash
# 1. Clone repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Django migrations (sessions, admin site, etc.)
python manage.py migrate

# 5. Initialize SQLAlchemy tables and seed admin
python manage.py initdb --admin-email admin@example.com --admin-password admin123

# 6. Run the development server
python manage.py runserver
```

👉 Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

Login with the seeded admin to manage products.  

---

## 🗄️ Database Schema  

**Users Table**  
- `id` (INTEGER, PK, autoincrement)  
- `email` (TEXT, unique)  
- `password` (TEXT, hashed)  
- `is_admin` (BOOLEAN, default `False`)  

**Products Table**  
- `id` (INTEGER, PK, autoincrement)  
- `name` (TEXT)  
- `description` (TEXT)  
- `price` (REAL)  
- `stock` (INTEGER)  
- `created_at` (TEXT)  
- `updated_at` (TEXT)  

---

## 🛠️ Tech Notes  

- **Django + SQLAlchemy** → Django handles sessions/auth; SQLAlchemy manages Users/Products with full ORM control.  
- **SQLite** → Single-file DB, no setup required.  
- **CSRF Protection** → CSRF tokens injected into Jinja forms with a `csrf_token` helper.  
- **Templating** → Jinja2 (with a `url()` helper to resolve Django routes).  
- **Admin Auth** → Simple `is_admin` flag for role-based product management.  

---

## 📦 Git/GitHub Workflow  

```bash
git init
git add .
git commit -m "Initial commit: Django + SQLAlchemy + Jinja CRUD"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
