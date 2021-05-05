from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Budget, City, Expenditure, PurchasePhotos
from .forms import ExpenditureForm, CityForm
from django.db.models import Q
import requests
from decimal import Decimal


import uuid
import boto3

from decouple import config

S3_BASE_URL = config('S3_BASE_URL')
BUCKET = config('BUCKET')
WEATHER_API_KEY = config('WEATHER_API_KEY')

# Home
def home(request):
    return render(request, 'pages/home.html')



# Sign Up form
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('budgets_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



# Show all budgets
def budgets_index(request):
  budgets = Budget.objects.filter(user=request.user)
  expenditure_form = ExpenditureForm()

  for budget in budgets:
    if budget.remaining_funds < (budget.initial_funds * .25):
      budget.color = '#cc3300'
    elif budget.remaining_funds < (budget.initial_funds * .50):
      budget.color = '#ff9966'
    elif budget.remaining_funds < (budget.initial_funds * .75):
      budget.color = '#ffcc00'
    elif budget.remaining_funds < (budget.initial_funds * .90):
      budget.color = '#99cc33'
    elif budget.remaining_funds >= (budget.initial_funds * .90):
      budget.color = '#339900'

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    city_weather = requests.get(url.format(budget.city, WEATHER_API_KEY)).json() #request the API data and convert the JSON to Python data types

    weather = {
      'temperature': city_weather['main']['temp'],
      'description': city_weather['weather'][0]['description'],
      'icon': city_weather['weather'][0]['icon']
    }

    budget.save()

  context = {
    'budgets': budgets,
    'expenditure_form': expenditure_form,
    'weather': weather
  }
  return render(request, 'pages/budget/index.html', context)

# Show budget details
def budget_detail(request, budget_id):
    budget = Budget.objects.get(id=budget_id)
    # below is how we only get the expenses that belong to this budget
    expenditures = Expenditure.objects.filter(budget = budget)
    total_expenses = 0
    # I want to add the expenses and save it in total-expenses variable
    for expenditure in expenditures:
      total_expenses += expenditure.amount
    # subtracting the expenses from my original budget
    after_expenses_budget = budget.initial_funds - total_expenses
    budget.remaining_funds = round(after_expenses_budget, 2)
    budget.total_spent = round(total_expenses, 2)
    budget.save()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    city_weather = requests.get(url.format(budget.city, WEATHER_API_KEY)).json() #request the API data and convert the JSON to Python data types

    weather = {
      'temperature': city_weather['main']['temp'],
      'description': city_weather['weather'][0]['description'],
      'icon': city_weather['weather'][0]['icon']
    }
    context = {
        'budget': budget,
        'total_expenses': round(total_expenses, 2),
        'after_expenses_budget': round(after_expenses_budget, 2),
        'weather': weather
    }
    return render(request, 'pages/budget/detail.html', context)


# Create new Budget
class BudgetCreate(CreateView):
  model = Budget
  fields = ['name', 'initial_funds', 'trip_destination', 'trip_description', 'city']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)



# Update Budget
class BudgetUpdate(UpdateView):
  model = Budget
  fields = ['initial_funds', 'trip_destination', 'trip_description', 'city']

# Delete Budget
class BudgetDelete(DeleteView):
  model = Budget
  success_url = '/budgets/'

# Add expenditure to Budget
def add_expense(request, budget_id):
  form = ExpenditureForm(request.POST)

  if form.is_valid():
    new_expense = form.save(commit=False)
    new_expense.budget_id = budget_id
    new_expense.save()
  return redirect('detail', budget_id=budget_id)

# Edit expenditure from Budget


# Delete expenditure from Budget
def remove_expense(request, budget_id, expense_id):
  budget = Budget.objects.get(id=budget_id)
  expenditures = Expenditure.objects.filter(budget = budget)
  for expenditure in expenditures:
    if expenditure.id == expense_id:
      expenditure.delete()
  return redirect('detail', budget_id=budget_id)

# Adding purchase photos
def add_trip_photo(request, budget_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            # budget = Budget.objects.get(id=budget_id)
            # print(budget, "budget printing")
            photo = PurchasePhotos(url=url, budget_id=budget_id)
            print(photo, "photo printing")
            print(photo.url)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', budget_id=budget_id)

# Function used for querying through budgets
def search_budgets(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups= Q(name__icontains=query) | Q(trip_destination__icontains=query) | Q(trip_description__icontains=query)
            budgets = Budget.objects.filter(user=request.user)

            results= budgets.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'pages/budget/index.html', context)

        else:
            return render(request, 'pages/budget/index.html')

    else:
        return render(request, 'pages/budget/index.html')

def search_expenses(request, budget_id):

  if request.method == 'GET':
    query= request.GET.get('q')

    submitbutton = request.GET.get('submit')

    if query is not None:
      lookups = Q(name__icontains=query) | Q(description__icontains=query) | Q(amount__icontains=query)
      budget = Budget.objects.get(id=budget_id)

      expenditures = Expenditure.objects.filter(budget = budget)

      results = expenditures.filter(lookups).distinct()

      context = {
        'results': results,
        'submitbutton': submitbutton,
        'budget': budget
      }
      return render(request, 'pages/budget/filtered_expenses.html', context)
    
    else:
      return render(request, 'pages/budget/filtered_expenses.html')

  else:
    return render(request, 'pages/budget/filtered_expenses.html')

# NOTE Getting the weather

def show_weather(request):
    cities = City.objects.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'


    if request.method == 'POST':
      form = CityForm(request.POST)
      form.save()

    form = CityForm()
    weather_data = []
    
    for city in cities:
      city_weather = requests.get(url.format(city.name, WEATHER_API_KEY)).json() #request the API data and convert the JSON to Python data types
      print(city_weather)
      weather = {
        'city': city.name,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
      }
      weather_data.append(weather)
    
    context = {
      'weather_data': weather_data,
      'form': form
    }
    return render(request, 'pages/weather_index.html', context) 