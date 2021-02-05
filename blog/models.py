from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class Post(models.Model):
	STATUS_CHOICE=(('draft','Draft'), ('published','Published'))
	title = models.CharField(max_length=200)
	author = models.ForeignKey(User , on_delete= models.CASCADE , related_name='blog_post')
	description = models.TextField()
	publish=models.DateTimeField( default= timezone.now)
	updated= models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True )
	slug= models.SlugField(max_length=256 , unique_for_date='publish')
	status = models.CharField(max_length=10 , choices = STATUS_CHOICE , default='draft')
	thumb = models.ImageField(default='blank.jpg' , blank=True)
	tag= TaggableManager() 

	class Meta:
		ordering= ('created',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('detail_display' , args= [self.publish.year , self.publish.strftime('%m'),self.slug])


class Comment(models.Model):
	name= models.CharField(max_length=60)
	post= models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	email= models.EmailField()
	desc= models.TextField()
	created= models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)

	class Meta:
		ordering=('created',)

	def __str__(self):
		return 'Commented by{}'.format(self.name)