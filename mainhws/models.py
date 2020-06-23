from django.db import models

class Article(models.Model):
	title=models.CharField(max_length=200)
	body=models.TextField(blank=True)
	date=models.CharField(max_length=200)
	slug=models.SlugField(unique=True,blank=True)

	def get_absolute_url(self): 
		return reverse('postcontent_url',kwargs={'slug':self.slug})