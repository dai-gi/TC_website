from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField('タイトル', max_length=200)
	text = models.TextField('内容')
	created_date = models.DateTimeField('作成日', default=timezone.now)
	published_date = models.DateTimeField('公開日', blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class Work(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField('タイトル', max_length=200)
	address = models.CharField('現場住所', max_length=200)
	content = models.TextField('作業内容', blank=True, null=True)
	staff = models.CharField('現場担当者', max_length=200, blank=True, null=True)
	tel = models.CharField('電話番号', max_length=200, blank=True, null=True)
	price = models.IntegerField('価格')
	created_date = models.DateTimeField('作成日', default=timezone.now)
	published_date = models.DateTimeField('公開日', blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title
