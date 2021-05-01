from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Budget(models.Model):
    name = models.CharField(max_length=100)
    initial_funds = models.IntegerField()
    trip_destination = models.CharField(max_length=60)
    trip_description = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'budget_id': self.id})

class Expenditure(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=255)
    amount = models.IntegerField()
    budget = models.ForeignKey(Budget, on_delete=CASCADE)
    date = models.DateField('Purchase date')

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.name} was purchased on {self.date}"

    # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'budget_id': self.id})