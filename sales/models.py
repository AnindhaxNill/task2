from django.db import models


# Create your models here.
class salesdb(models.Model):
    order_id = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    ship_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    ship_mode = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    segment = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.IntegerField()
    region = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    sales = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self) -> str:
        return self.order_id
