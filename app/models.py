from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField('タイトル', max_length=200)
	image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True) 
	text = models.TextField('内容')
	created_date = models.DateTimeField('作成日', default=timezone.now)
	published_date = models.DateTimeField('公開日', blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title