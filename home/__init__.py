from django.db import models
import secrets        
import string
from decimal import Decimal
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

def generate_coupon_code(model_class, length=CODE_LENGTH):
    while True:
        code = ''.join(secrets.choice(ALPHANUMERIC_CHARS) for i in range(length))
        if not model_class.objects.filter(code=code).exists():
            return code

class ActiveOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__in=['pending', 'processing'])

ALPHANUMERIC_CHARS = string.ascii_uppercase + string.digits
CODE_LENGTH = 10

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="The unique code for the coupon.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):

        if not self.pk and not self.code:
            self.code = generate_coupon_code(self.__class__, length=CODE_LENGTH)

        super().save(*args, **kwargs)    

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code

class Order(models.Model):

        """Model for a customer order."""

        STATUS_CHOICES = [
            ('pending', 'Pending payment'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ]

        objects = models.Manager()
        active_orders = ActiveOrderManager()

        created_at = models.DateTimeField(auto_now_add=True)
        total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='pending',
            db_index=True
        )
    
        class Meta:
            ordering = ['-created_at']
            verbose_name = "Order"
            verbose_name_plural = "Orders"

        def __str__(self):
            return f"Order #{self.pk} - {self.get_status_display()}"
class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name    