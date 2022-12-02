from django.contrib import admin
from .models import register_main, register_payment
# Register your models here.
admin.site.register(register_main)
admin.site.register(register_payment)
