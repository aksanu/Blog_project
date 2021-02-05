from django import template
from blog.models import Post
register = template.Library()


@register.simple_tag
def total_count():
	return Post.objects.count()

@register.inclusion_tag('temp.html')
def latest_post():
	latest= Post.objects.order_by('-created')[:5]
	return {'latest':latest}