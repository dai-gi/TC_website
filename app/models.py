from django.conf import settings
from django.db import models
from django.urls import reverse

class Post(models.Model):
	image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True) 
	title = models.CharField('タイトル', max_length=200)
	text = models.TextField('内容')
	price = models.CharField('料金', max_length=50)

	def __str__(self):
		return self.title