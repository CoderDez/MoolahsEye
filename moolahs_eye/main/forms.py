from .models import Budget, Item
from django.forms import ModelForm

class BudgetForm(ModelForm):

    def __init__(self,*args,**kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        # override class for bootstrap purposes

        classes = {
            'user_id': 'hider',
            'name': 'form-control',
            'amount': 'form-control',
            'frequency': 'form-select'
        }
        for field in ["user_id", "name", "amount", "frequency"]:
            self.fields[field].widget.attrs.update(
                {
                    'class': f'{classes[field]}'
                })

    class Meta:
        model = Budget
        fields = ["user_id", "name", "amount", "frequency"]

class ItemForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        classes = {
            "budget_id": "hider",
            "name": "form-control",
            "cost": "form-control",
            "frequency": "form-select",
            "category": "form-select"
        }
        for field in ["budget_id","name", "cost", "frequency", "category"]:
            self.fields[field].widget.attrs.update(
                {
                    "class": f"{classes[field]}"
                }
            )

    class Meta:
        model = Item
        fields = ["budget_id","name", "cost", "frequency", "category"]


