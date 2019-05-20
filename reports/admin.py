from django.contrib import admin

from .models import Report
from .models import Category

admin.site.register(Report)
admin.site.register(Category)