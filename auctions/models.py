from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', blank=True, related_name="userWatchlist")

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Auction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField('date', default=timezone.now)
    starting_price = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', verbose_name='image', blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id} : >> Owner << {self.user.username} >>, Start ${self.starting_price}, Title << {self.title} >> at {self.date}"


class Bid(models.Model):
    myproduct = models.ForeignKey('Auction', on_delete=models.CASCADE)
    date_bid = models.DateTimeField('date_bid', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_price = models.DecimalField(decimal_places=2, max_digits=5)  

    def __str__(self):
        return f"{self.id} | {self.bid_price} | {self.user} | {self.date_bid} : {self.myproduct}"

class Comment(models.Model):
    date_comment = models.DateTimeField('date_comment', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    myproduct = models.ForeignKey('Auction', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

