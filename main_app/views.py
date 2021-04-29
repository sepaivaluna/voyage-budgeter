from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Budget, Expenditure
from .forms import ExpenditureForm

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
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



# Show all budgets
def budgets_index(request):
  budgets = Budget.objects.all()
  expenditure_form = ExpenditureForm()
  context = {
    'budgets': budgets,
    'expenditure_form': expenditure_form 
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



# Update Budget
class BudgetUpdate(UpdateView):
    model = Budget
    fields = ['initial_funds', 'trip_destination', 'trip_description']



# Add expenditure to Budget
def add_expense(request, budget_id):
  form = ExpenditureForm(request.POST)

  if form.is_valid():
    new_expense = form.save(commit=False)
    new_expense.budget_id = budget_id
    new_expense.save()
  return redirect('detail', budget_id=budget_id)