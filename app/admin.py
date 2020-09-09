from django.contrib import admin
from .models import Post, Work, Category, WorkCategory

admin.site.register(Post)
admin.site.register(Work)
admin.site.register(Category)
admin.site.register(WorkCategory)

