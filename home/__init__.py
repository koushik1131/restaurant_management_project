from django.db import models
import secrets        
import string

ALPHANUMBERIC_CHARS = string.ascii_uppercase + string.digits
def generate_coupon_code(length=10, max_attempts=10):

    if length <=0:
        raise ValueError("Coupon code length must be greater than zero.")

    for attempt in range(max_attempts):
        code = ''.join(secrets.choice(ALPHANUMBERIC_CHARS) for _ in range(length))

        if not Coupon.objects.filter(code=code).exists():
            return code

    raise RuntimeError(
        f"could not generate a unique coupon code after {max_attempts} attempts."
        "consider incerasing the length the length or max_attempts."
    )            

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.pk and not self.code:
            self.code = generate_coupon_code()

from decimal import Decimal
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return slef.code

    class ActiveOrderManager(models.manager):

        def get_active_orders(self):

            return self.filter(status__in=['pending', 'processing'])

    class ActiveOrderManager(models.Manager):

    created_at = models.DataTimeField(auto_now_add=True)
        def get_active_orders(self):
            return self.filter(status__in=['pending', 'processing'])        
        verbose_name_plural = "Orders"
    class Order(models.Model):

        STATUS_CHOICES = [
            ('pending', 'Pending payment'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ]
            return f"Order #{self.pk} = ..."
        created_at = models.DataTimeField(auto_now_add=True)
        total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='pendig',
            db_index=True
        )

        objects = ActiveOrderManager()

        class Meta:
            ordering = ['-created_at']
            verbose_name = "Order"
            verbose_name_plural = "Orders"

        def __str__(self):
            return f"Order #{self.pk} - {self.get_status_display()}"    