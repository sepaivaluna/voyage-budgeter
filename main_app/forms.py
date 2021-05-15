from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import NumberInput, Select, TextInput, Textarea
from .models import City, Expenditure, Budget, Review
from django import forms

class ExpenditureForm(ModelForm):
    class Meta:
        model = Expenditure
        fields = ['name', 'description', 'amount', 'date']

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        # widgets = {
        #     'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        # } #updates the input class to have the correct Bulma class and placeholder

class UpdateBudgetForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = Budget
        # specify fields to be used
        fields = ['name', 'initial_funds', 'trip_destination', 'trip_description', 'city', 'theme']
        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'initial_funds': NumberInput(attrs={'class':'form-control', 'min':'0'}),
            'trip_destination': TextInput(attrs={'class':'form-control'}),
            'trip_description': Textarea(attrs={'class':'form-control', 'rows':'4'}),
            'city': TextInput(attrs={'class':'form-control'}),
            'theme': Select(attrs={'class':'form-select'}),
        }

class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'message']
        widgets = {
            'title': TextInput(attrs={'class':'form-control'}),
            'rating': Select(attrs={'class':'form-select'}),
            'message': Textarea(attrs={'class':'form-control', 'rows':'4'})
        }