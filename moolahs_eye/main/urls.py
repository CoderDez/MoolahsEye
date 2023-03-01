from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('home/', views.home_view, name="home"),
    path("new_budget", views.new_budget_view, name="new_budget"),
    path("edit_budget", views.edit_budget_view, name="edit_budget"),
    path("delete_budget", views.delete_budget_view, name="delete_budget"),
]