from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return self.username

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateField(blank=True, null=True)
    ending_time = models.DateField(blank=True, null=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='bids')

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    time = models.DateField()

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    bid_time = models.DateTimeField()