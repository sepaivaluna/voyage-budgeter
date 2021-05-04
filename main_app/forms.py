from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import City, Expenditure

class ExpenditureForm(ModelForm):
    class Meta:
        model = Expenditure
        fields = ['name', 'description', 'amount', 'date']

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        } #updates the input class to have the correct Bulma class and placeholder