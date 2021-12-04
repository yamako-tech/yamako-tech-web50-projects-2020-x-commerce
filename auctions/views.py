from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Max
from django.db import IntegrityError
from django.shortcuts import render
from django.utils import timezone

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import User, Category, Auction, Bid, Comment
from .forms import *


def index(request):
    product = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "objects": product
    })


def all(request):
    product = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "objects": product
    })


@login_required
def newproduct(request):
    if request.method == 'POST':
        user = request.user
        category = Category.objects.get(id=request.POST["category"])
        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        image = forms.ImageField(label='image', required=False)
        new_product = Auction.objects.create(
            title=title, category=category, date=timezone.now(), starting_price=starting_price, description=description, user=user, image=image, active=True)
        new_product.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/new_product.html", {
        'categories': Category.objects.all()
    })


def detail(request, id):
    item = Auction.objects.get(id=id)
    bids = Bid.objects.filter(myproduct=item)
    comments = Comment.objects.filter(myproduct=item)
    value = bids.aggregate(Max('bid_price'))['bid_price__max']
    bid = None
    if value is not None:
        bid = Bid.objects.filter(bid_price=value)[0]
    return render(request, "auctions/detail.html", {
        'item': item,
        'bids': bids,
        'comments': comments,
        'bid': bid
    })


def category(request):
    if request.method == 'POST':
        category = request.POST["category"]
        new_category, created = Category.objects.get_or_create(
            name=category.lower())
        if created:
            new_category.save()
        else:
            messages.warning(request, "Category already Exists!")
        return HttpResponseRedirect(reverse("category"))
    return render(request, "auctions/category.html", {
        'category': Category.objects.all()
    })


def search(request, name):
    category = Category.objects.get(name=name)
    product = Auction.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "objects": product
    })


@login_required
def comment(request, id):
    if request.method == 'POST':
        myproduct = Auction.objects.get(id=id)
        user = request.user
        text = request.POST["content"].strip()
        if(text != ""):
            comment = Comment.objects.create(date_comment=timezone.now(
            ), user=user, myproduct=myproduct, text=text)
            comment.save()
        return HttpResponseRedirect(reverse("detail", kwargs={'id': id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def bid(request, id):
    if request.method == 'POST':
        myproduct = Auction.objects.get(id=id)
        bid_price = request.POST["bid"]
        args = Bid.objects.filter(myproduct=myproduct)
        value = args.aggregate(Max('bid_price'))['bid_price__max']
        if value is None:
            value = 0
        if float(bid_price) < myproduct.starting_price or float(bid_price) <= value:
            messages.warning(
                request, f'Bid must be higher than: ${max(value, myproduct.starting_price)}!')
            return HttpResponseRedirect(reverse("detail", kwargs={'id': id}))
        user = request.user
        bid = Bid.objects.create(
            date_bid=timezone.now(), user=user, bid_price=bid_price, myproduct=myproduct)
        bid.save()
    return HttpResponseRedirect(reverse("detail", kwargs={'id': id}))


@login_required
def newproduct(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.owner = user
            new_product.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/newproduct.html", {
                "form": form
            })
    else:
        return render(request, "auctions/newproduct.html", {
            "form": ProductForm()
        })


@login_required
def close(request, itemId):
    myproduct = Auction.objects.get(id=itemId)
    user = request.user
    if myproduct.user == user:
        myproduct.active = False
        myproduct.save()
        messages.success(
            request, f'{myproduct.title} auction is closed.')
    else:
        messages.info(
            request, 'Only the owner can close this auction.')
    return HttpResponseRedirect(reverse("detail", kwargs={'id': myproduct.id}))


@login_required
def watchlist(request, pk):
    if request.method == 'POST':
        user = request.user      
        myproduct = Auction.objects.get(id=pk)
        if request.POST["status"] == '1':
            user.watchlist.add(myproduct)
        else:
            user.watchlist.remove(myproduct)
        user.save()
        return HttpResponseRedirect(
            reverse("detail", kwargs={'id': myproduct.id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def watch(request):
    user = request.user
    product = user.watchlist.all()
    return render(request, "auctions/index.html", {
        "objects": product
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


@login_required
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