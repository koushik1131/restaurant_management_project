from django.db import models
import secrets        
import string
from decimal import Decimal
from django.db.models import Manager

class ActiveOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__in=['pending', 'processing'])

ALPHANUMERIC_CHARS = string.ascii_uppercase + string.digits

class  Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="The unique code for the coupon.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.pk and not self.code:
            self.code = generate_coupon_code()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.code            

def generate_coupon_code(length=10, max_attempts=10):
    if length <=0:
        raise ValueError("Coupon code length must be greater than zero.")

    for attempt in range(max_attempts):
        code = ''.join(secrets.choice(ALPHANUMERIC_CHARS) for _ in range(length))

        if not Coupon.objects.filter(code=code).exists():
            return code

    raise RuntimeError(
        f"could not generate a unique coupon code after {max_attempts} attempts."
        "consider increasing the length or max_attempts."
    )            

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="The unique code for the coupon.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):

        if not self.pk and not self.code:
            self.code = generate_coupon_code()

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
        objects = models.Manager()

        active_orders = ActiveOrderManager()

        class Meta:
            ordering = ['-created_at']
            verbose_name = "Order"
            verbose_name_plural = "Orders"

        def __str__(self):
            return f"Order #{self.pk} - {self.get_status_display()}"    