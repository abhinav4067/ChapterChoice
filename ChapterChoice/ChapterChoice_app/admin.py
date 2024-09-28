from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Book)
admin.site.register(user_reg)
admin.site.register(review)

        