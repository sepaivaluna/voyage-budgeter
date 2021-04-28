from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # budget urls
    path('budgets/', views.budgets_index, name='index'),
    path('budgets/<int:budget_id>/', views.budget_detail, name='detail'),

    # user urls
    path('accounts/signup/', views.signup, name='signup'),
]