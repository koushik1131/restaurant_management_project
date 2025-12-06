from django.db import models
import secrets        
import string
from decimal import Decimal
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _

def generate_coupon_code(model_class, length=CODE_LENGTH):
    while True:
        code = ''.join(secrets.choice(ALPHANUMERIC_CHARS) for i in range(length))
        if not model_class.objects.filter(**{field_name:code}).exists():
            return code

class ActiveOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__in=['pending', 'processing'])

ALPHANUMERIC_CHARS = string.ascii_uppercase + string.digits
CODE_LENGTH = 10
ORDER_ID_CHAR = string.digits
ORDER_ID_LENGTH = 10

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
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return self.code

class PaymentMethod(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("A clear name for the payment method (e.g., 'Credit Card', 'Cash').")
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("A bried explanation of the payment method.")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Indicated if the payment method is currently available.")
    )

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")
        ordering = ['name']
    def __str__(self):
        return self.name    

class Order(models.Model):

        """Model for a customer order."""

        STATUS_CHOICES = [
            ('pending', _('Pending payment')),
            ('processing', _('Processing')),
            ('shipped', ('Shipped')),
            ('delivered', _('Delivered')),
            ('cancelled', _('Cancelled')),
        ]

        objects = models.Manager()
        active_orders = ActiveOrderManager()

        order_number = models.CharField(
            max_length=15,
            unique=True,
            editable=False,
            verbose_name=_("Oreder Number")
        )

        created_at = models.DateTimeField(auto_now_add=True)
        total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='pending',
            db_index=True
        )
        coupon = models.ForeignKey(
            Coupon,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            help_text="Coupon applied to this order."
        )
        def save(self, *args, **kwargs):
            if not self.pk and not self.order_number:
                self.order_number = generate_order_number(self.__class__)
            super().save(*args, **kwargs)    
    
        class Meta:
            ordering = ['-created_at']
            verbose_name = _("Order")
            verbose_name_plural = _("Orders")

        def __str__(self):

            return f"Order #{self.pk} - {self.get_status_display()}"

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Restaurant")
        verbose_name_plural = _("Restaurants")

    def __str__(self):
        return self.name    

class LoyaltyProgram(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Tier Name"),
        help_text=_("The unique name of the loyalty tier (e.g., Bronze, Silver).")
    )
    points_required = models.IntegerField(
        unique=True,
        verbose_name=_("Points Required"),
        help_text=_("The minimum number of loyalty points required to reach this tier.")
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Discount Percentage"),
        help_text=_("The percentage discout customer in this tier receive.")
    )
    description = models.TextField(
        verbose_name=_("Benefits Description"),
        help_text=_("A brief explanation of the benefits for this tier.")
    )

    class Meta:
        ordering = ['points_required']
        verbose_name= _("Loyalty program Tier")
        verbose_name_plural = _("Loyalty Program Tiers")
    def __str__(self):
        return f"{self.name} ({self.points_required} pts)"    