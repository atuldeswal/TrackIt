from django.db import models
from django.contrib.auth import get_user_model

# Retrieve the custom user model
User = get_user_model()

class Products(models.Model):
    # Many-to-Many relationship with the User model. A product can be associated with multiple users and vice versa.
    user = models.ManyToManyField(User)
    # CharField for storing the name of the product.
    product_name = models.CharField(max_length=255)
    # URLField for storing the product's online location, unique to ensure no duplicate product URLs.
    product_url = models.URLField(unique=True)
    # URLField for storing the URL of the product's image.
    product_img = models.URLField()
    # IntegerField for storing the product's price.
    product_price = models.IntegerField()
    # DateField for storing the date when the product was added to the database.
    date_added = models.DateField()
    
    class Meta:
        # Custom names for the Product model in the Django admin site
        verbose_name = "Product"
        verbose_name_plural = "Products"

class PriceUpdate(models.Model):
    # ForeignKey linking to a Product. CASCADE means if the referenced Product is deleted, delete this too.
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    # DateField for storing the date of the price update.
    dates = models.DateField()
    # IntegerField for the new price of the product.
    price = models.IntegerField()

class TrackingStatus(models.Model):
    # BooleanField indicating whether tracking is active or not, defaults to False.
    is_tracking = models.BooleanField(default=False, verbose_name="Is Tracking Active")

    def __str__(self):
        # Human-readable string representation of the model, indicating tracking status.
        return "Tracking is currently " + ("active" if self.is_tracking else "inactive")

    class Meta:
        # Custom name for the TrackingStatus model in the Django admin site, ensuring correct pluralization.
        verbose_name_plural = "Tracking Status"
