from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Budget

# Create your views here.


def home(request):
    return render(request, 'pages/home.html')

# User Sign Up form

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def budgets_index(request):
  budgets = Budget.objects.all()
  context = {
    'budgets': budgets
  }
  return render(request, 'pages/budget/index.html', context)


def budget_detail(request, budget_id):
    budget = Budget.objects.get(id=budget_id)
    context = {
        'budget': budget
    }
    return render(request, 'pages/budget/detail.html', context)