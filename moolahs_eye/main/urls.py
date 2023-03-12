from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login_view"),
    path('dashboard/<int:id>', views.dashboard_view, name="dashboard_view"),

    path("new_budget/", views.new_budget_view, name="new_budget_view"),
    path("edit_budget/<int:id>", views.edit_budget_view, name="edit_budget_view"),
    path("delete_budget/<int:id>", views.delete_budget_view, name="delete_budget_view"),

    path("edit_item/<int:budget_id>/<int:item_id>", views.edit_item_view, name="edit_item_view"),
    path("new_item/<int:budget_id>", views.new_item_view, name="new_item_view"),
    path("delete_item/<int:budget_id>/<int:item_id>", views.delete_item_view, name="delete_item_view"),

    path("calculator/<int:budget_id>", views.calculator_view, name="calculator_view")
]