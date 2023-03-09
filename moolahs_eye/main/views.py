from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
                return redirect('dashboard_view', id=0)
        else:
            return render(
                req, "login.html", {"error_message": "Invalid credentials. Try again."})
    if req.method == "GET":
        if hasattr(req, "user"):
            if isinstance(req.user, User):
                logout(req) 
        return render(req, "login.html")

def dashboard_view(req, id=-0):
    budget = req.user.budget_set.filter(id=id).first()
    budgets = req.user.budget_set.exclude(id=id)
        
    if budget:
        items = budget.item_set.all()
        return render(
            req, "dashboard.html",
            {"budgets": budgets, "budget": budget, "items": items}
        )
    elif budgets:
        items = budgets[0].item_set.all()
        return render(
            req, "dashboard.html",
            {"budgets": budgets, "budget": budgets[0], "items": items}
        )
    else:
        return redirect("new_budget_view")


def new_budget_view(req):
    context = {}
    if req.method == "GET":
        context["budget_form"] = BudgetForm(initial = {"user_id": req.user.id})
        return render(req, "dashboard.html", context)
    else:
        form = BudgetForm(req.POST)
        if form.is_valid():
            try:
                budget = form.save(commit=True)
                messages.success(req, message=f"{budget.name} has been created.")
                return redirect("dashboard_view", id=budget.id)
            except Exception as e:
                pass
        for error in form.errors:
            messages.error(req, error)
        context["budget_form"] = form
        return render(req, "dashboard.html", context)

def edit_budget_view(req, id):
    context = {}
    budget = Budget.objects.filter(id=id).first()
    if budget:
        if req.method == "GET":
            context["budget_form"] = BudgetForm(instance=budget, initial = {"user_id": req.user.id})
            return render(req, "dashboard.html", context)
        else:
            try:
                form = BudgetForm(req.POST, instance=budget)
                if form.is_valid():
                    form.save()
                    return redirect("dashboard_view", id=id)
                else:
                    for error in form.errors:
                        messages.error(req, error)
            except:
                pass
            context["budget_form"] = BudgetForm(req.POST)
            return render(req, "dashboard.html", context)
        
        
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
        return redirect('dashboard_view', id=0)


def edit_item_view(req, budget_id, item_id):
    context = {}
    item = Item.objects.filter(id=item_id).first()
    print("item: ", item)
    if item:
        budget = Budget.objects.filter(id=budget_id).first()
        print("budget: ", budget)
        if budget:
            context["budget"] = budget
            context["items"] = budget.item_set.exclude(id=item.id)
            context["item"] = item
            if req.method == "GET":
                context["item_form"] = ItemForm(instance=item, initial = {"budget_id": budget})
                return render(req, "dashboard.html", context)
            else:
                try:
                    form = BudgetForm(req.POST, instance = item)
                    if form.is_valid():
                        form.save()
                        return redirect("dashboard_view", id=budget_id)
                    else:
                        for error in form.errors:
                            messages.error(req, error)
                except:
                    pass

                context["item_form"] = Item(req.POST)
                return render(req, "dashboard.html", context)

def new_item_view(req, budget_id):
    context = {}
    budget = Budget.objects.filter(id=budget_id).first()
    if budget:
        context["budget"] = budget
        context["items"] = budget.item_set.all()
        if req.method == "GET":
            context["item_form"] = ItemForm(initial = {"budget_id": budget})
            return render(req, "dashboard.html", context)
        else:
            form = ItemForm(req.POST)
            if form.is_valid():
                try:
                    item = form.save(commit=True)
                    messages.success(req, message=f"{item.name} has been created.")
                    return redirect("new_item_view", budget_id=budget.id)
                except:
                    pass
        for error in form.errors:
            messages.error(req, error)
        context["item_form"] = form
        return render(req, "dashboard.html", context)

def delete_item_view(req, budget_id, item_id):
    try:
        item = Item.objects.filter(id=item_id).first()
        if item:
            item.delete()
    except:
        pass

    return redirect("dashboard_view", id=budget_id)




