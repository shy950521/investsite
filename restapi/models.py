from django.db import models
from django.contrib.auth.models import User


# stock detail
class Stock(models.Model):
    name = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10, primary_key=True)
    price = models.FloatField(max_length=100)

    def __str__(self):
        return str(self.name) + ' ' + str(self.ticker)


# user -(1) invest (n) - stock
class Invest(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    share = models.FloatField(max_length=100)

    def __str__(self):
        return str(self.user) + ' ' + str(self.ticker) + ' ' + str(self.share) + ' ' + str(self.pk)


# user customized detail
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(max_length=150, default=10000.00)

    def __str__(self):
        return str(self.user) + str(self.balance)


# user input history
class Receive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first = models.CharField(max_length=10)
    second = models.CharField(max_length=10)
    third = models.CharField(max_length=10)
    fourth = models.CharField(max_length=10)
    fifth = models.CharField(max_length=10)
    val  = models.FloatField(max_length=150)
    time = models.DateTimeField(auto_now_add=True)

# Create your models here.
