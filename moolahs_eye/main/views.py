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
        breakdown = budget.get_categorical_breakdown()
        data_points = budget.get_data_points()
        return render(
            req, "dashboard.html",
            {"budgets": budgets, "budget": budget, 
             "items": items, "breakdown": breakdown,
             "data_points": data_points
            }
        )
    elif budgets:
        items = budgets[0].item_set.all()
        breakdown = budgets[0].get_categorical_breakdown()
        data_points = budgets[0].get_data_points()
        return render(
            req, "dashboard.html",
            {"budgets": budgets, "budget": budgets[0], 
             "items": items, "data_points": data_points}
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
                messages.error(req, e)
        
        for error in form.errors:
            messages.error(req, error)

        context["budget_form"] = form
        return render(req, "dashboard.html", context)

def edit_budget_view(req, id):
    context = {}
    budget = Budget.objects.filter(id=id).first()
    if budget:
        context["budget"] = budget
        context["items"] = budget.item_set.all()
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
            except Exception as e:
                messages.error(req, e)
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
    if item:
        budget = Budget.objects.filter(id=budget_id).first()
        if budget:
            context["budget"] = budget
            context["items"] = budget.item_set.exclude(id=item.id)
            context["item"] = item
            if req.method == "GET":
                context["item_form"] = ItemForm(instance=item, initial = {"budget_id": budget})
                return render(req, "dashboard.html", context)
            else:
                try:
                    form = ItemForm(req.POST, instance = item)
                    if form.is_valid():
                        form.save()
                        return redirect("dashboard_view", id=budget_id)
                    else:
                        for error in form.errors:
                            print(error)
                            messages.error(req, error)
                except:
                    pass

                context["item_form"] = ItemForm(req.POST)
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


def calculator_view(req, budget_id):
    try:
        context = {}
        budget = Budget.objects.filter(id=budget_id).first()
        if budget:
            context["budget"] = budget
            if budget.item_set.all():
                context["frequencies"] = budget.item_set.all().first().get_frequencies()
            else:
                context["frequencies"] = budget.get_budget_frequencies()

            if req.method == "GET":
                context["frequency"] = budget.get_frequency()
                context["items"] = budget.get_item_costs(context["frequency"])
                print(context["items"])
                if context["items"]:
                    context["amount"] = budget.get_total_costs(context["frequency"])
                else:
                    context["amount"] = 0
                return render(req,"calculator.html", context)
            
            elif req.method == "POST":
                context["frequency"] = req.POST.get("frequency")
                context["items"] = budget.get_item_costs(context["frequency"])
                if context["items"]:
                    context["amount"] = budget.get_total_costs(context["frequency"])
                else:
                    context["amount"] = 0
                
            return render(req,"calculator.html", context)

    except Exception as e:
        print(e)
        pass

    return redirect("dashboard_view", id=budget_id)



