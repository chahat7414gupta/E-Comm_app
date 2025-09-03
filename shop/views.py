from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .db import SessionLocal
from .models_sa import Product, User


# --- List Products (all users) ---
class ProductListView(View):
    def get(self, request):
        with SessionLocal() as db:
            products = db.query(Product).order_by(Product.id.desc()).all()

        return render(
            request,
            "products.jinja.html",
            {"products": products, "user": request.session.get("user")},
        )


# --- Create Product (admin only) ---
class ProductCreateView(View):
    def get(self, request):
        user = request.session.get("user")
        if not user or not user.get("is_admin"):
            return HttpResponseForbidden("Only admins can create products.")
        return render(request, "product_form.jinja.html", {"action": "Create", "user": user})

    def post(self, request):
        user = request.session.get("user")
        if not user or not user.get("is_admin"):
            return HttpResponseForbidden("Only admins can create products.")

        with SessionLocal() as db:
            product = Product(
                name=request.POST["name"],
                description=request.POST.get("description"),
                price=float(request.POST["price"]),
                stock=int(request.POST["stock"]),
            )
            db.add(product)
            db.commit()

        return redirect("product_list")


# --- Edit Product (admin only) ---
class ProductEditView(View):
    def get(self, request, product_id):
        user = request.session.get("user")
        if not user or not user.get("is_admin"):
            return HttpResponseForbidden("Only admins can edit products.")

        with SessionLocal() as db:
            product = db.query(Product).filter_by(id=product_id).first()

        return render(
            request,
            "product_form.jinja.html",
            {"action": "Edit", "product": product, "user": user},
        )

    def post(self, request, product_id):
        user = request.session.get("user")
        if not user or not user.get("is_admin"):
            return HttpResponseForbidden("Only admins can edit products.")

        with SessionLocal() as db:
            product = db.query(Product).filter_by(id=product_id).first()
            if product:
                product.name = request.POST["name"]
                product.description = request.POST.get("description")
                product.price = float(request.POST["price"])
                product.stock = int(request.POST["stock"])
                db.commit()

        return redirect("product_list")


# --- Delete Product (admin only) ---
@method_decorator(csrf_exempt, name="dispatch")
class ProductDeleteView(View):
    def post(self, request, product_id):
        user = request.session.get("user")
        if not user or not user.get("is_admin"):
            return HttpResponseForbidden("Only admins can delete products.")

        with SessionLocal() as db:
            product = db.query(Product).filter_by(id=product_id).first()
            if product:
                db.delete(product)
                db.commit()

        return redirect("product_list")


# --- Register User ---
class RegisterView(View):
    def get(self, request):
        return render(request, "register.jinja.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        with SessionLocal() as db:
            existing_user = db.query(User).filter_by(email=email).first()
            if existing_user:
                return HttpResponse("⚠️ User already exists with this email.", status=400)

            # ✅ store plain text password
            user = User(email=email, password=password, is_admin=False)
            db.add(user)
            db.commit()

        return redirect("login")


# --- Login User ---
class LoginView(View):
    def get(self, request):
        return render(request, "login.jinja.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        with SessionLocal() as db:
            user = db.query(User).filter_by(email=email).first()

            # ✅ plain text check
            if not user or user.password != password:
                return HttpResponse("❌ Invalid email or password", status=401)

            # Save user in session
            request.session["user"] = {
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin,
            }

        return redirect("product_list")


# --- Logout User ---
class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("login")
