from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    name_company = models.CharField(max_length=60)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    
    choices = (
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    )
    field = models.CharField(max_length=30, blank=False,
                             null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name
    

class Service_Request(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    service_id =models.IntegerField()
    adress = models.CharField(max_length=100)
    nbre_hour = models.DecimalField(decimal_places=1, max_digits=100)
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    service_name= models.TextField()
    name_company= models.TextField()
    total_price = models.DecimalField(decimal_places=2, max_digits=100)
    field= models.TextField()
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return str(self.user_id)
