from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Budget, Expenditure, PurchasePhotos
from .forms import ExpenditureForm

import uuid
import boto3

# Using this to sort the dates
from django.db.models import DateTimeField
from django.db.models.functions import Trunc

S3_BASE_URL = "https://s3-us-east-2.amazonaws.com/"
BUCKET = "voyagebudgeter"

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

    print(budget.color)
    budget.save()
  context = {
    'budgets': budgets,
    'expenditure_form': expenditure_form 
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
    budget.remaining_funds = after_expenses_budget
    budget.total_spent = total_expenses
    budget.save()
    context = {
        'budget': budget,
        'total_expenses': total_expenses,
        'after_expenses_budget': after_expenses_budget
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
def add_purchase_photo(request, budget_id):
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