from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductEditView,
    ProductDeleteView,
    LoginView,
    RegisterView,
    LogoutView,
)

urlpatterns = [
    # Auth routes
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Product routes
    path("", ProductListView.as_view(), name="product_list"),
    path("products/new/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:product_id>/edit/", ProductEditView.as_view(), name="product_edit"),
    path("products/<int:product_id>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
