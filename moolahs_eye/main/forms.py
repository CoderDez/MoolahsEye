from .models import Budget, Item
from django.forms import ModelForm

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ["name", "amount", "frequency"]

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "cost", "frequency", "category"]


