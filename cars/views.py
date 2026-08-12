from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Car


def home(request):
    featured_cars = Car.objects.filter(featured=True)
    latest_cars = Car.objects.order_by("-id")[:6]

    return render(request, "home.html", {
        "featured_cars": featured_cars,
        "latest_cars": latest_cars,
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "Username या password गलत है"
        })

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def buy_cars(request):
    query = request.GET.get("q", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    min_year = request.GET.get("min_year", "").strip()
    company = request.GET.get("company", "").strip()
    year = request.GET.get("year", "").strip()

    cars = Car.objects.all()

    if query:
        cars = cars.filter(
            Q(company__icontains=query) |
            Q(model__icontains=query)
        )

    if max_price:
        cars = cars.filter(price__lte=max_price)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if company:
        cars = cars.filter(company=company)

    if year:
        cars = cars.filter(year=year)

    return render(request, "buy.html", {
    "cars": cars,
    "query": query,
    "max_price": max_price,
    "min_year": min_year,
    "company": company,
    "year": year,
})

@login_required
def sell_car(request):
    if request.method == "POST":
        Car.objects.create(
            seller=request.user,
            company=request.POST.get("company"),
            model=request.POST.get("model"),
            year=request.POST.get("year"),
            price=request.POST.get("price"),
            description=request.POST.get("description"),
            phone=request.POST.get("phone"),
            image=request.FILES.get("image"),
        )
        return redirect("buy_cars")

    return render(request, "sell.html")


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    return render(request, "car_detail.html", {
        "car": car
    })


@login_required
def my_cars(request):
    cars = Car.objects.filter(seller=request.user)
    return render(request, "my_cars.html", {
        "cars": cars
    })


@login_required
def edit_car(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        seller=request.user
    )

    if request.method == "POST":
        car.company = request.POST.get("company")
        car.model = request.POST.get("model")
        car.year = request.POST.get("year")
        car.price = request.POST.get("price")
        car.description = request.POST.get("description")
        car.phone = request.POST.get("phone")
        car.save()

        return redirect("my_cars")

    return render(request, "edit_car.html", {
        "car": car
    })


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        seller=request.user
    )

    if request.method == "POST":
        car.delete()
        return redirect("my_cars")

    return render(request, "delete_car.html", {
        "car": car
    })
from .models import Wishlist

@login_required
def toggle_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        car=car
    )

    if not created:
        wishlist.delete()

    return render(request, 'buy.html', {
    'cars': cars,
    'query': query,
    'max_price': max_price,
    'min_year': min_year,
    'company': company,
    'year': year,
})
@login_required
def my_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"wishlist": wishlist})
@login_required
def profile(request):
    total_cars = Car.objects.filter(seller=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request, "profile.html", {
        "total_cars": total_cars,
        "wishlist_count": wishlist_count,
    })
