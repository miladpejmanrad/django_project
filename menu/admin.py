from django.contrib import admin
from menu.models import Category, MenuItem, Order, Allergen, AdminMenu, Notification, Drink, DrinkFlavor, DrinkOrder

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Allergen)
admin.site.register(AdminMenu)
admin.site.register(Notification)
admin.site.register(Drink)
admin.site.register(DrinkFlavor)
admin.site.register(DrinkOrder)