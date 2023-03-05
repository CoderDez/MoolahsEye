from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login_view"),
    path('dashboard/<int:id>', views.dashboard_view, name="dashboard_view"),
    path("new_budget/<int:id>", views.new_budget_view, name="new_budget_view"),
    path("edit_budget/<int:id>", views.edit_budget_view, name="edit_budget_view"),
    path("delete_budget/<int:id>", views.delete_budget_view, name="delete_budget_view"),
]