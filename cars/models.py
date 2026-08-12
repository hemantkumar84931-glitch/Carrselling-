from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    company = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.company} {self.model}"
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "car")
