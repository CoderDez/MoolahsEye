from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Budget, Item, User
from .forms import BudgetForm, ItemForm

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

def home_view(req, pk=None):
    budgets = req.user.budget_set.all()
    if not len(budgets):
        return redirect("/new_budget")
    else:
        return render(req, "items.html", {budgets})

def new_budget_view(req):
    context = {}
    if req.method == "GET":
        context["form"] = BudgetForm()
        return render(req, "budget_form.html", context)
    else:
        form = BudgetForm(req.POST)
        if form.isvalid():
            try:
                form.save()
                redirect("/home")
            except Exception as e:
                context["form"] = BudgetForm()
                context["error_message"] = e
                return render(req, "budget_form.html", context)

def edit_budget_view(req, pk):
    budget = Budget.objects.filter(id=pk)
    if budget:
        if req.method == "GET":
            context = {}
            context["form"] = BudgetForm(instance=budget)
            return render(req, "budget_form.html", context)
        else:
            try:
                form = BudgetForm(req.POST, instance=budget)
                if form.isvalid():
                    form.save()
                    redirect("/home")
            except Exception as e:
                context["form"] = BudgetForm(instance=budget)
                context["error_message"] = e
                return render(req, "budget_form.html")
        
        
def delete_budget_view(req, pk):
    try:
        budget = Budget.objects.filter(id=pk).first()
        if budget:
            budget.delete()
    except:
        pass

    return redirect("/home")


def edit_item_view(req, pk):
    item = Item.objects.filter(id=pk)
    if req.method == "GET":
        context = {"form": ItemForm(instance=item)}
        return render(req, "items.html", req)
    else:
        return 


def new_item_view(req, pk):
    pass

def delete_item_view(req, pk):
    try:
        item = Item.objects.filter(id=pk).first()
        if item:
            item.delete()
    except:
        pass

    return redirect("/home")




