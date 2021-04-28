from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Budget

# Home
def home(request):
    return render(request, 'pages/home.html')

# Sign Up form
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

# Show all budgets
def budgets_index(request):
  budgets = Budget.objects.all()
  context = {
    'budgets': budgets
  }
  return render(request, 'pages/budget/index.html', context)

# Show budget details
def budget_detail(request, budget_id):
    budget = Budget.objects.get(id=budget_id)
    context = {
        'budget': budget
    }
    return render(request, 'pages/budget/detail.html', context)

# Create new Budget
class BudgetCreate(CreateView):
  model = Budget
  fields = ['name', 'initial_funds', 'trip_destination', 'trip_description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)