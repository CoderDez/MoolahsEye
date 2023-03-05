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
            budget = user.budget_set.all().first()
            if budget:
                return redirect('dashboard_view', id=budget.id)
            else:
                return redirect('dashboard_view', id=-1)
        else:
            return render(
                req, "login.html", {"error_message": "Invalid credentials. Try again."})
    if req.method == "GET":
        if hasattr(req, "user"):
            if isinstance(req.user, User):
                logout(req) 
        return render(req, "login.html")

def dashboard_view(req, id=-1):
    budgets = req.user.budget_set.all()
    if not len(budgets):
        return redirect("/new_budget")
    else:
        return render(req, "dashboard.html", {"budgets": budgets, "budget": budgets[0]})

def new_budget_view(req):
    context = {}
    if req.method == "GET":
        context["budget_form"] = BudgetForm()
        return render(req, "dashboard.html", context)
    else:
        form = BudgetForm(req.POST)
        if form.isvalid():
            try:
                form.save()
                # find how to get the budget that's just being saved id
                redirect("dashboard_view")
            except Exception as e:
                context["form"] = BudgetForm()
                context["error_message"] = e
                return render(req, "dashbaord.html", context)

def edit_budget_view(req, id):
    budget = Budget.objects.filter(id=id).first()
    if budget:
        if req.method == "GET":
            context = {"budget": budget}
            context["budget_form"] = BudgetForm(instance=budget)
            return render(req, "dashboard.html", context)
        else:
            try:
                form = BudgetForm(req.POST, instance=budget)
                if form.isvalid():
                    form.save()
                    redirect("dashboard_view", id=id)
            except Exception as e:
                context["form"] = BudgetForm(instance=budget)
                context["error_message"] = e
                return render(req, "dashboard.html")
        
        
def delete_budget_view(req, id):
    try:
        budget = Budget.objects.filter(id=id).first()
        if budget:
            budget.delete()
    except:
        pass
    
    budget = req.user.budget_set.all().first()
    if budget:
        return redirect('dashboard_view', id=budget.id)
    else:
        return redirect('dashboard_view', id=-1)


def edit_item_view(req, id):
    item = Item.objects.filter(id=id)
    if req.method == "GET":
        context = {"form": ItemForm(instance=item)}
        return render(req, "items.html", req)
    else:
        return 


def new_item_view(req, id):
    pass

def delete_item_view(req, id):
    try:
        item = Item.objects.filter(id=id).first()
        if item:
            item.delete()
    except:
        pass

    return redirect("/home")




