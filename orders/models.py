from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
class regularPizza(models.Model):
    items = models.CharField(max_length=20)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.items} - {self.small}|{self.large}"

    class Meta:
        verbose_name_plural = "Regular Pizza"

class sicilianPizza(models.Model):
    items = models.CharField(max_length=20)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.items} - {self.small}|{self.large}"

    class Meta:
        verbose_name_plural = "Sicilian Pizza"

class Toppings(models.Model):
    topp = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.topp}"

    class Meta:
        verbose_name_plural = "Toppings"

class Subs(models.Model):
    items = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.items} - {self.small}|{self.large}"

    class Meta:
        verbose_name_plural = "Subs"

class Pasta(models.Model):
    items = models.CharField(max_length=40)
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.items} - {self.rate}"

    class Meta:
        verbose_name_plural = "Pasta"

class Salad(models.Model):
    items = models.CharField(max_length=40)
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.items} - {self.rate}"

    class Meta:
        verbose_name_plural = "Salad"

class dinnerPlatters(models.Model):
    items = models.CharField(max_length=20)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.items} - {self.small}|{self.large}"

    class Meta:
        verbose_name_plural = "Dinner Platters"

class Orders(models.Model):
    email = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    selection = models.CharField(max_length=64)
    size = models.CharField(max_length=20, null=True)
    topping = models.CharField(max_length=150, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    progress = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.email} ordered {self.category} | {self.selection} | {self.topping}"
    
    class Meta:
        verbose_name_plural = "Pending Orders"

class Credits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.user} - {self.credit}"

    class Meta:
        verbose_name_plural = "Credits"