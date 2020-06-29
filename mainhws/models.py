from django.conf import settings
from django.db import models
from django.utils import timezone

class Article(models.Model):
	title=models.CharField(max_length=200)
	body=models.TextField(blank=True)
	date=models.CharField(max_length=200)
	author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	published_date=models.DateTimeField(blank=True, null=True)

	def __str__(self): return self.title+" | "+self.body

	def get_absolute_url(self): 
		return reverse('postcontent_url',kwargs={'pk':self.pk})