from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Budget, Category, Item, User


def login_view(req):    
    if req.method == "POST":
        email = req.POST.get("email")
        password = req.POST.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(req, user)
            return redirect("/home")
        else:
            return render(
                req, "login.html", {"error_message": "Invalid credentials. Try again."})
    if req.method == "GET":
        if hasattr(req, "user"):
            if isinstance(req.user, User):
                logout(req) 
        return render(req, "login.html")

@login_required
def home_view(req):
    context = get_context(req)
    if req.method == "GET":
        return render(req, "home.html", context)

def get_context(req):
    context = {}
    budgets = req.user.get_budgets()
    budget = budgets.first()
    budget_frequencies = Budget.get_frequencies()
    categories = Category.objects.all()
    if budget:
        if len(budget.item_set.all()):
            context["item_frequencies"] = budget.item_set.all()[0].get_frequencies(limit=True)
        else:
            context["item_frequencies"] = []
    context["budget"] = budget
    context["budgets"] = budgets
    context["budget_frequencies"] = budget_frequencies
    context["categories"] = categories
    return context

