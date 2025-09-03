
from django.core.management.base import BaseCommand
from shop.db import engine, Base, SessionLocal
from shop.models_sa import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Initialize SQLAlchemy tables and create an admin user"

    def add_arguments(self, parser):
        parser.add_argument('--admin-email', type=str, default='admin@example.com')
        parser.add_argument('--admin-password', type=str, default='admin123')

    def handle(self, *args, **options):
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            email = options['admin_email'].strip().lower()
            password = options['admin_password']
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                admin = User(email=email, password=make_password(password), is_admin=True)
                db.add(admin)
                db.commit()
                self.stdout.write(self.style.SUCCESS(f"Created admin {email}"))
            else:
                self.stdout.write(self.style.WARNING(f"Admin {email} already exists"))
        finally:
            db.close()
        self.stdout.write(self.style.SUCCESS("Database initialized"))
