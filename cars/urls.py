from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('buy/', views.buy_cars, name='buy_cars'),
    path('sell/', views.sell_car, name='sell_car'),
    path("my-cars/", views.my_cars, name="my_cars"),
    path('logout/', views.logout_view, name='logout'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('my-cars/', views.my_cars, name='my_cars'),
    path('car/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('car/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path("wishlist/<int:car_id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("my-wishlist/", views.my_wishlist, name="my_wishlist"),
    path("profile/", views.profile, name="profile"),
]

