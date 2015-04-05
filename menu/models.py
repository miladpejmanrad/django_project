from django.db import models
from django.db.models import Sum

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

# MenuItem class. Defines our menu items and their relationships to other classes.
class MenuItem(models.Model):
	# Set up the choices for the allergens field.
	allergen_choices = (
		('peanuts', 'Peanuts'),
		('tree-nuts', 'Tree nuts'),
		('milk', 'Milk'),
		('eggs', 'Eggs'),
		('gluten', 'Gluten'),
		('soy', 'Soy'),
		('fish', 'Fish'),
		('shellfish', 'Shellfish')
	)
	vegetarian = models.BooleanField(default=False)
	category = models.ForeignKey(Category) # This sets up a many-to-one relationship with the Category class
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	main_photo = models.ImageField(upload_to = 'menu/items/')
	allergens = models.CharField(max_length=512, choices=allergen_choices)
	
	# This sets the name as the main identifier for the object.
	# e.g. "Bacon-wrapped Shrimp" will show up in the admin panel instead of an ID number
	def __str__(self):
		return str(self.name)

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
	menu_items = models.ManyToManyField(MenuItem) # Defines a many-to-many relationship with the MenuItems class
	table_number = models.IntegerField()
	modifications = models.TextField(blank=True)
	status = models.CharField(max_length=64, choices=status_choices, default='ordering')
	total_price = models.DecimalField(max_digits=8, decimal_places=2)
	timestamp_created = models.DateTimeField(auto_now_add=True)

	# Sets the ID as the identifier for orders.
	def __str__(self):
		return str(self.id)
		
		

# Class Survey
class Survey(models.Model):

#Setting up the survey class, initialize setups some default variables such as the variables below,
#since they will always be used when a survey is created. 

#TJ
	
	def __init__(self, serviceRating, foodRating, orderRating, customerComments):
		self.serviceRating = serviceRating
		self.foodRating = foodRating
		self.orderRating = orderRating
		self.customerComments = customerComments

	def printRating(self):
		print("Service Rating: ")

	def __unicode__(self):
		return self.id
