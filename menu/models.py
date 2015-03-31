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
	category = models.ForeignKey(Category)
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	main_photo = models.ImageField(upload_to = 'menu/items/')
	def __unicode__(self):
		return self.name
		
class Order(models.Model):
	status_choices = (
	        ('in-progress', 'In Progress'),
	        ('cooking', 'Cooking'),
	        ('ready-to-serve', 'Ready to Serve'),
	        ('served', 'Served'),
	        ('paid', 'Paid')
        )
	menu_items = models.ManyToManyField(MenuItem)
	table_number = models.IntegerField()
	modifications = models.TextField()
	status = models.CharField(max_length=64, choices=status_choices, default='in-progress')
	total_price = models.DecimalField(max_digits=8, decimal_places=2)
	timestamp_created = models.DateTimeField(auto_now_add=True)
