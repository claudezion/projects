from django.contrib.auth import authenticate , login , logout
from django.db import IntegrityError
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from datetime import datetime

from .models import User, Item , Category , Bid , Watchlist , Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Item.objects.filter(status="True"),
        "head": "Active Listings"
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
    if request.method == "POST":
        title = (request.POST)['title']
        description = (request.POST)['description']
        starting_bid = (request.POST)['starting_bid']
        url = (request.POST)['url']
        category = (request.POST)['category']
        user_id = (request.POST)['user_id']
        try:
            query = Item(title=title, description=description, starting_bid=starting_bid, current_bid=0, current_bid_user_id=0, url=url, category=category, user_id=user_id, status="True")
            query.save()
            messages.success(request, 'Your item has been listed')
            return render(request, "auctions/listing.html", {
                "listings": Item.objects.filter(title=title, description=description, starting_bid=starting_bid, url=url, category=category, user_id=user_id, status="True")
            })
        except:
            messages.error(request, 'Invalid Entry')
            return render(request, "auctions/create_listing.html", {
                "categories": Category.objects.all()
            })
    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def watchlist(request):
    if request.method == "POST":
        item_id = (request.POST)['item_id']
        user_id = (request.POST)['user_id']
        title = (request.POST)['title']
        try:
            entry = Watchlist.objects.get(user_id=user_id, item_id=item_id, title=title)
            entry.delete()
            messages.success(request, 'Removed the item from the watchlist')
            return render(request, "auctions/listing.html", {
                "listings": Item.objects.filter(pk=item_id),
                "comments": Comment.objects.filter(item_id=item_id),
                "logs": Bid.objects.filter(item_id=item_id)
            })
        except:
            query = Watchlist(item_id=item_id, user_id=user_id, title=title)
            query.save()
            messages.success(request, 'Added to the watchlist')
            return render(request, "auctions/listing.html", {
                "listings": Item.objects.filter(pk=item_id),
                "comments": Comment.objects.filter(item_id=item_id),
                "logs": Bid.objects.filter(item_id=item_id)
            })


def listing(request, id):
    if request.method == "POST":
        user_name = (request.POST)['user_name']
        starting_bid = (request.POST)['starting_bid']
        current_bid = (request.POST)['current_bid']
        bid = (request.POST)['bid']
        title = (request.POST)['title']
        if not bid:
            messages.error(request, 'Invalid Entry')
            return render(request, "auctions/listing.html", {
                "listings": Item.objects.filter(pk=id),
                "logs": Bid.objects.filter(item_id=id),
                "comments": Comment.objects.filter(item_id=id)
            })
        elif float(bid) < float(starting_bid) or float(bid) != float(starting_bid) and float(bid) <= float(current_bid):
            messages.warning(request, 'Your bid should at least be equal or grater than the starting bid and should be grater than the current bid if any ')
            return render(request, "auctions/listing.html", {
                "listings": Item.objects.filter(pk=id),
                "logs": Bid.objects.filter(item_id=id),
                "comments": Comment.objects.filter(item_id=id)
            })
        else:
            query = Item.objects.get(pk=id)
            query.current_bid = bid
            query.save()
            query.current_bid_user_id = (request.POST)['user_id']
            query.save()
            history = Bid(item_id=id, user_name=user_name, bid=bid)
            history.save()
            messages.success(request, 'You have bidden successfully')
            if Watchlist.objects.filter(item_id=id).exists():
                return render(request, "auctions/listing.html", {
                    "listings": Item.objects.filter(pk=id),
                    "logs": Bid.objects.filter(item_id=id),
                    "comments": Comment.objects.filter(item_id=id)
                })
            else:
                query = Watchlist(item_id=id, user_id=(request.POST)['user_id'], title=title)
                query.save()
                messages.success(request, 'Added to the watchlist')
                return render(request, "auctions/listing.html", {
                    "listings": Item.objects.filter(pk=id),
                    "logs": Bid.objects.filter(item_id=id),
                    "comments": Comment.objects.filter(item_id=id)
                })
    return render(request, "auctions/listing.html", {
        "listings": Item.objects.filter(pk=id),
        "comments": Comment.objects.filter(item_id=id),
        "logs": Bid.objects.filter(item_id=id)
    })


def category(request):
    return render(request, "auctions/index.html", {
        "listings": Item.objects.filter(category=(request.POST)['name'], status="True"),
        "head": (request.POST)['name']
    })


def comment(request):
    if request.method == "POST":
        item_id = (request.POST)['item_id']
        user_name = (request.POST)['user_name']
        comment = (request.POST)['comment']
        query = Comment(item_id=item_id, user_name=user_name, comment=comment)
        query.save()
        return render(request, "auctions/listing.html", {
            "listings": Item.objects.filter(pk=item_id),
            "comments": Comment.objects.filter(item_id=item_id),
            "logs": Bid.objects.filter(item_id=item_id)
        })


def close(request):
    if request.method == "POST":
        item_id = (request.POST)['item_id']
        query = Item.objects.get(pk=item_id)
        query.status = "False"
        query.save()
        return render(request, "auctions/listing.html", {
                "listings": Item.objects.filter(pk=item_id),
                "comments": Comment.objects.filter(item_id=item_id),
                "logs": Bid.objects.filter(item_id=item_id)
            })
    else:
        return render(request, "auctions/index.html", {
            "listings": Item.objects.filter(status="False"),
            "head": "Closed Listings"
        })


def list(request):
    if request.method == "POST":
        return render(request, "auctions/watchlist.html", {
            "list": Watchlist.objects.filter(user_id=(request.POST)['user_id'])
        })