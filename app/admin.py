from django.contrib import admin
from .models import Post, Work, PostCategory, WorkCategory

admin.site.register(Post)
admin.site.register(Work)
admin.site.register(PostCategory)
admin.site.register(WorkCategory)

