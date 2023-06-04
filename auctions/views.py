from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from .models import User, AuctionListing
from .forms import ListingForm
from django.contrib import messages
from django.shortcuts import render, redirect


def index(request):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=request.POST["listing_id"])
        if request.POST["form_type"]=="bid":
            bid_amount = float(request.POST["bid_amount"])
            if (not listing.highest_bidder and bid_amount<listing.current_price) or bid_amount<=listing.current_price:
                messages.error(request, "Please Increase your bid to exceed the minimum amount")
            else:
                #listing.highest_bidder = User.objects.get(pk=int(request.POST["bidder_id"]))
                listing.highest_bidder = request.user
                listing.current_price = bid_amount
                listing.save()
        elif request.POST["form_type"]=="add_to_watchlist":
            #user = User.objects.get(pk=int(request.POST["user_id"]))
            if request.user.watchlist.filter(id=request.POST["listing_id"]).exists():
                messages.error(request, "The listing is already in your watchlist")
            else:
                request.user.watchlist.add(listing)
                messages.success(request, 'Listing added to watchlist.')

    return render(request, "auctions/index.html", { 
        "listings": AuctionListing.objects.all()
    })


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
    
def create_listing(request):
    owner = request.user
    if not owner.is_authenticated:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = owner
            listing.save()
            return redirect('index')
    else:
        form = ListingForm()
    
    return render(request, 'auctions/create_listing.html', {'form': form})

def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method == 'POST':
        request.user.watchlist.remove(request.POST["listing_id"])
        messages.success(request, 'Listing removed from watchlist.')
    return render(request, "auctions/watchlist.html", { 
        "watchlist": request.user.watchlist.all()
    })