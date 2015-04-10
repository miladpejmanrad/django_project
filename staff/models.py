from django.db import models
from django.contrib.auth.models import User
from menu.models import Order 
# Create your models here.


class CookStatus(models.Model):
	cook_name = models.ForeignKey(User)
	current_order = models.ForeignKey(Order, blank=True, null=True)
