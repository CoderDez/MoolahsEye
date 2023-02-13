from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Budget, Category, Item, User


def login(req):    
    if req.method == "POST":
        email = req.POST.get("email")
        password = req.POST.get("password")
        valid = User.is_credentials_valid(email, password)
        if valid == True:
            user = User.objects.get(email = email)
            login(req, user)
            return redirect("/reports")
        else:
            return render(
                req, "login.html", {"error_message": "Invalid credentials. Try again."})
    if req.method == "GET":
        if hasattr(req, "user"):
            if isinstance(req.user, User):
                logout(req) 
        return render(req, "login.html")

@login_required
def home(req):
    context = get_context(req)

def get_context(req):
    context = {}
    
    user = None # get user
    budgets = Budget.objects.filter(user_id = user.id)
    budget = budgets.first()
    if budget:
        item_frequencies = budget.item_set.all()[0].get_frequencies(limit=True)
    else:
        item_frequencies = budget.item_set.all()[0].get_frequencies()
    
    budget_frequencies = Budget.get_frequencies()
    categories = Category.objects.all()

    context["budget"] = budget
    context["budgets"] = budgets
    context["budget_frequencies"] = budget_frequencies
    context["item_frequencies"] = item_frequencies
    context["categories"] = categories

    return context

