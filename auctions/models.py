from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    startingbid = models.IntegerField()
    currentbid = models.IntegerField() # Initialise to starting bid somehow? Reference a bid object?
    active = models.BooleanField(default=True)

    # Many-to-one relationship with user should be def'd here
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Many-to-one relationship with category def'd here 


    # Many-to-many relationship with being in a user's watchlist 
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    # URL for image 
    imageurl = models.URLField(blank=True)

    # RETURN STRING 
    def __str__(self):
        return f"{self.id}: {self.title} with starting bid {self.startingbid}, listed by {self.owner}"

class Bid(models.Model):
    value = models.IntegerField()

    # Many-to-one relationship with the user making the bid 
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, default=0, related_name="bids")

    # Many-to-one relationship with Listing
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
# add classes for listings, bids and comments (and categories)