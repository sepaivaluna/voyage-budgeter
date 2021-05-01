from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # budget urls
    path('budgets/', views.budgets_index, name='budgets_index'),
    path('budgets/create/', views.BudgetCreate.as_view(), name="create_budget"),
    path('budgets/<int:budget_id>/', views.budget_detail, name='detail'),
    path('budgets/<int:pk>/update/', views.BudgetUpdate.as_view(), name='update_budget'),
    path('budgets/<int:pk>/delete/', views.BudgetDelete.as_view(), name="delete_budget"),

    # expense urls
    path('budgets/<int:budget_id>/add_expense', views.add_expense, name="add_expense"),
    path('budgets/<int:budget_id>/remove_expense/<int:expense_id>/', views.remove_expense, name='remove_expense'),

    # user urls
    path('accounts/signup/', views.signup, name='signup'),
]