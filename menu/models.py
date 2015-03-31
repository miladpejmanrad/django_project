from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=200)
	main_photo = models.ImageField(upload_to = 'menu/categories/')
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "categories"

class MenuItem(models.Model):
	#allergen_choices = (
	#	('peanuts', 'Peanuts'),
	#	('tree-nuts', 'Tree nuts'),
	#	('milk', 'Milk'),
	#	('eggs', 'Eggs'),
	#	('gluten', 'Gluten'),
	#	('soy', 'Soy'),
	#	('fish', 'Fish'),
	#	('shellfish', 'Shellfish')
	#)
	vegetarian = models.BooleanField(default=False)
	category = models.ForeignKey(Category)
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	main_photo = models.ImageField(upload_to = 'menu/items/')
	#allergens = models.CharField(max_length=64, choices=allergen_choices, default='none')
	def __unicode__(self):
		return self.name
		
class Order(models.Model):
	#status_choices = (
	#        ('in-progress', 'In Progress'),
	#        ('cooking', 'Cooking'),
	#        ('ready-to-serve', 'Ready to Serve'),
	#        ('served', 'Served'),
	#        ('paid', 'Paid')
        #)
	#menu_items = models.ManyToManyField(MenuItem)
	table_number = models.IntegerField()
	modifications = models.TextField()
	#status = models.CharField(max_length=64, choices=status_choices, default='in-progress')
	total_price = models.DecimalField(max_digits=8, decimal_places=2)
	timestamp_created = models.DateTimeField(auto_now_add=True)
#<<<<<<< HEAD

# Class Survey
#class Survey(models.Model):
'''
Setting up the survey class, initialize setups some default variables such as the variables below,
since they will always be used when a survey is created. 

TJ
	
'''
	'''def __init__(self, serviceRating, foodRating, orderRating, customerComments):
		self.serviceRating = serviceRating
		self.foodRating = foodRating
		self.orderRating = orderRating
		self.customerComments = customerComments
=======
	def __unicode__(self):
		return self.id
>>>>>>> origin/master '''
