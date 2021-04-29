from django.forms import ModelForm
from .models import Expenditure


class ExpenditureForm(ModelForm):
    class Meta:
        model = Expenditure
        fields = ['name', 'description', 'amount']
