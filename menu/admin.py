from django.contrib import admin
from menu.models import Category, MenuItem, Order, Allergen, AdminMenu

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Allergen)
admin.site.register(AdminMenu)