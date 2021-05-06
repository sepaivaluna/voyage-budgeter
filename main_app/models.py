from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

RELAX_THEMES = (('Kittens', 'Kittens'), ('Puppies', 'Puppies'))

class City(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self): #show the actual city name on the dashboard
        return f'{self.name} for user_id: {self.user.id}' 


class Budget(models.Model):
    name = models.CharField(max_length=100)
    initial_funds = models.IntegerField()
    trip_destination = models.CharField(max_length=60)
    trip_description = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remaining_funds = models.IntegerField(null=True)
    total_spent = models.IntegerField(null=True)
    color = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=25, null=True)
    theme = models.CharField(max_length=7, choices=RELAX_THEMES, default=RELAX_THEMES[0][0], null=True)
    percentage_difference = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'budget_id': self.id})

    class Meta:
        ordering = ['name']

class Expenditure(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=255)
    amount = models.FloatField()
    budget = models.ForeignKey(Budget, on_delete=CASCADE)
    date = models.DateField('Purchase date')

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.name} was purchased on {self.date}"

    # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'budget_id': self.id})

    class Meta:
        ordering = ['-date']

class PurchasePhotos(models.Model):
    url = models.CharField(max_length=200)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for budget_id: {self.budget_id} @{self.url}'