from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return **self.code**

import secrets        
import string
from django.conf import settings
from .models import Coupon

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

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return **slef.code**        