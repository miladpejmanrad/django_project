from django.db import models
from django.contrib.auth.models import User, Group



# Create your models here.
# NOTE: Syncdb will NOT create tables/columns for MODIFIED classes in 1.6.
# It only creates tables/columns for NEW classes. If you are modifying a class that already exists,
# you will need to either recreate the database or use the South app
# (http://south.readthedocs.org/en/latest/tutorial/part1.html) to set up a migration
# so columns for new or modified fields will be added to the database.

# Category class. Defines the categories that menu items fall under.
class Category(models.Model):
	name = models.CharField(max_length=200)
	# main_photo = models.ImageField(upload_to = 'menu/categories/')
	
	# This sets the name as the main identifier for the object.
	# e.g. "Appetizers" will show up in the admin panel instead of an ID number
	def __str__(self):
		return str(self.name)

	# This sets the plural name, so it's not "Categorys"
	class Meta:
		verbose_name_plural = "categories"

# Allergens class. Surprisingly, there isn't a model field for a multiple choice field.
# Documentation recommends creating a separate class for choices you need to select multiples of.
class Allergen(models.Model):
	ingredient = models.CharField(max_length=64)
	
	def __str__(self):
		return str(self.ingredient)
		
# MenuItem class. Defines our menu items and their relationships to other classes.
class MenuItem(models.Model):
	visible = models.BooleanField(default=True) # This controls whether or not the menu item shows up on the customer-facing menu
	vegetarian = models.BooleanField(default=False)
	low_calorie = models.BooleanField(default=False)
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	main_photo = models.ImageField(upload_to = 'menu/items/')
	category = models.ForeignKey(Category) # This sets up a many-to-one relationship with the Category class
	description = models.TextField()
	ingredients = models.TextField(blank=True)
	allergens = models.ManyToManyField(Allergen)
	
	# This sets the name as the main identifier for the object.
	# e.g. "Bacon-wrapped Shrimp" will show up in the admin panel instead of an ID number
	def __str__(self):
		return str(self.name)
		
# DrinkFlavors class. This provides the flavor options for the drinks.
class DrinkFlavor(models.Model):
	flavor = models.CharField(max_length=200)
	def __str__(self):
		return str(self.flavor)

# Drink class. Similar to a MenuItem, but simpler.
class Drink(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	category = models.ForeignKey(Category)
	def __str__(self):
		return str(self.name)

# DrinkOrder class. This collects the information for an ordered drink into one object to be added to an Order.
class DrinkOrder(models.Model):
	drink = models.ForeignKey(Drink)
	flavor = models.ForeignKey(DrinkFlavor, blank=True, null=True)
	def __str__(self):
		if str(self.flavor) != 'None':
			return str(self.flavor) + ' ' + str(self.drink.name)
		else:
			return str(self.drink.name)

# Order class. Defines our orders and their relationships to other classes.
class Order(models.Model):
	# Sets up the available choices for the status field.
	status_choices = (
		('ordering', 'Ordering'),
	        ('in-progress', 'In Progress'),
	        ('cooking', 'Cooking'),
	        ('ready-to-serve', 'Ready to Serve'),
	        ('served', 'Served'),
	        ('paid', 'Paid')
    	)
	menu_items = models.ManyToManyField(MenuItem, blank=True) # Defines a many-to-many relationship with the MenuItems class
	drinks = models.ManyToManyField(DrinkOrder, blank=True) # Defines a many-to-many relationship with the DrinkOrder class
	table_number = models.IntegerField()
	modifications = models.TextField(blank=True)
	status = models.CharField(max_length=64, choices=status_choices, default='ordering')
	total_price = models.DecimalField(max_digits=8, decimal_places=2)
	tip = models.DecimalField(max_digits=8, decimal_places=2, default='0.00')
	timestamp_created = models.DateTimeField(auto_now_add=True)

	# related chef name
	chef =  models.CharField(max_length=64, blank=True, null=True)

	# Sets the ID as the identifier for orders.
	def __str__(self):
		return str(self.id)

	
# Notifications class. This sets up notification objects that can be displayed to the wait staff.
class Notification(models.Model):
	type_choices = (
		('help', 'Help'),
		('refill', 'Refill'),
		('ready', 'Ready to serve'),
		('cash', 'Pay with cash')
	)
	table_number = models.IntegerField()
	type = models.CharField(max_length=64, choices=type_choices, default='help')
	drink = models.CharField(max_length=64, blank=True) # This is an optional field
	order = models.ForeignKey(Order, blank=True, null=True)
	# Sets the ID as the identifier for notifications
	def __str__(self):
		return str(self.id)

	

# Class Survey
class Survey(models.Model):
	

	rating = (
		('very bad', 'Very Bad'),
	        ('bad', 'Bad'),
	        ('not so bad', 'Not So Bad'),
	        ('good', 'Good'),
	        ('very good', 'Very Good')
    	)
	server = models.CharField(max_length=64, choices=rating, default='good')
	food = models.CharField(max_length=64, choices=rating, default='good')
	ordering = models.CharField(max_length=64, choices=rating, default='good')
	Comments = models.TextField(blank=True)

	def __unicode__(self):
		return str(self.id)

class AdminMenu(models.Model):
	options = models.CharField(max_length=64)
	
	def __str__(self):
		return str(self.options)


class CookStatus(models.Model):
	"""
	 model descripting which order is cooking by wich kitchen
	"""
	cook_name = models.ForeignKey(User) 
	current_order = models.ForeignKey(Order, blank=True, null=True)

