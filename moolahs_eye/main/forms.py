from .models import Budget, Item
from django.forms import ModelForm

class BudgetForm(ModelForm):

    def __init__(self, *args,**kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        # override class for bootstrap purposes
        for field in ["name", "amount", "frequency"]:
            classes = {
                'name': 'form-control',
                'amount': 'form-control',
                'frequency': 'form-select'
            }
            self.fields[field].widget.attrs.update(
                {
                    'class': f'{classes[field]}'
                })

    class Meta:
        model = Budget
        fields = ["name", "amount", "frequency"]

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "cost", "frequency", "category"]


