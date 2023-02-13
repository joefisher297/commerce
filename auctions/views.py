from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
        })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing
        })


def watchlist(request):
    if request.method == "POST":
        user_id = (request.POST["userid"])
        listing_id = (request.POST["listingid"])

        listing = Listing.objects.get(id=listing_id)
        user = User.objects.get(id=user_id)

        # If the hidden html form with "add" has been submitted:
        if request.POST["changelist"] == "Add to Watchlist":
            user.watchlist.add(listing)
            return HttpResponseRedirect(reverse('listing', args=(),kwargs={'listing_id': listing_id}))

        # Likewise for "remove"
        elif request.POST["changelist"] == "Remove From Watchlist":
            user.watchlist.remove(listing)
            return HttpResponseRedirect(reverse('listing', args=(),kwargs={'listing_id': listing_id}))

        # Catch-all does nothing
        else:
            return HttpResponseRedirect(reverse('listing', args=(),kwargs={'listing_id': listing_id}))

    # A GET request will return the watchlist page
    else:
        return render(request, "auctions/watchlist.html")


def create(request):

    # If the create form has just been submitted we can take out all the data
    if request.method=="POST":

        title = request.POST["title"]
        description = request.POST["description"]
        startingbid = request.POST["startingbid"]
        imageurl = request.POST["imageurl"]
        user_id = request.POST["ownerid"]
        owner = User.objects.get(id=user_id)


        newlisting = Listing(title=title, description=description, startingbid=startingbid, currentbid=startingbid, imageurl=imageurl, owner=owner)
        newlisting.save()

        return HttpResponseRedirect(reverse('index'))


    else:
        return render(request, "auctions/create.html")

def bid(request):

    # Pulling all the data out of a new bid request 
    if request.method == "POST":
        newbid = int(request.POST["newbid"])
        bidder_id = request.POST["bidder_id"]
        bidder = User.objects.get(id=bidder_id)
        listing_id = request.POST["listing_id"]

        listing = Listing.objects.get(id=listing_id)

        if listing.currentbid >= newbid:
            messages.warning(request, "Your new bid must be greater than the current bid on the listing")
            return HttpResponseRedirect(reverse('listing', args=(),kwargs={'listing_id': listing_id}))

        else:
            b = Bid(value=newbid, bidder=bidder, listing=listing)
            b.save()
            listing.currentbid = newbid
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=(),kwargs={'listing_id': listing_id}))

    else:
        return HttpResponseRedirect(reverse('listing'))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
