from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
	list_display = ['title','slug','author','publish','updated','created','status']
	date_hierarchy ='created'
	prepopulated_fields = {"slug": ("title",)}
	list_filter=('status','author')
	search_fields=['title']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
	list_display=['name','post','email','desc','updated','created','active']
	date_hierarchy='created'
	list_filter=('active','name')
	search_fields=['email']
admin.site.register(Comment,CommentAdmin)

