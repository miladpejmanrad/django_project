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