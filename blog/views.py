from django.shortcuts import render , get_object_or_404,redirect
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.



def list_display(request, tag_slug=None):
	if request.method == "POST":
		if 'search' in request.POST:
			search= request.POST['search']
			print(type(search))
			post_list= models.Post.objects.filter(status= 'published' ,author__username= str(request.POST['search']))
			return render(request,'list_display.html',{'post_list':post_list})

	if not request.user.is_authenticated:
		return redirect('login')
	else:
		post_list= models.Post.objects.filter(author= request.user)
		tag= None
		if tag_slug:
			tag= get_object_or_404(Tag, slug=tag_slug)
			post_list=post_list.filter(tag__in=[tag])


		paginator= Paginator(post_list , 4)
		page_num = request.GET.get('page')
		
		try:
			posts = paginator.page(page_num)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)

		return render(request,'list_display.html', {'post_list':post_list, 'post_list':posts , 'tag':tag})
	

		

def detail_display(request, year,month,post):
	post= get_object_or_404(models.Post , slug=post,
										 status='published',
										  publish__year=year,
										  publish__month=month)

	comment = post.comments.filter(active=True)
	
	if request.method=='POST':
		name= request.POST['Name']
		email= request.POST['Email']
		message= request.POST['message']
		data= models.Comment.objects.get_or_create(name=name , post=post , email=email , desc=message)
		


	return render(request , 'detail.html',{'posts':post, 'comments':comment})

def send_email(request,id ):
	email = get_object_or_404(models.Post , status='published',id=id)
	sent= False
	if sent == False:
		if request.method == 'POST':
			name= request.POST['Name']
			sender_email1= request.POST['Your_Email']
			to= request.POST['To']
			message = request.POST['body']
			subject= '{} recommends you to read {}'.format(name,email.title)
			post_url= request.build_absolute_uri(email.get_absolute_url())
			message1 = 'Click here to read the post: {} \n\n Message by: "{}" \n {} \n {}'.format(post_url, name, message, sender_email1)
			send_mail(subject, message1, sender_email1, [to] , fail_silently=False)

			sent=True

	


	return render(request,'email.html',{'sent':sent})



def CreatePost(request):
	
	if request.method == 'POST' and request.FILES['image']:
		title= request.POST['title']
		myfile = request.FILES['image']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		description= request.POST['desc']
		current_user= request.user
		slug= slugify(title)
		status= request.POST['status']
		tag1= request.POST['tag1']
		tag2= request.POST['tag2']
		tag3= request.POST['tag3']

		data = models.Post(title=title , author=current_user,
												 description=description,
												 slug=slug, 
												 status=status,
												 thumb=myfile, 
												 )
		data.save()

		data.tag.add(tag1,tag2,tag3)

	return render(request, 'post_create.html')


num1= None
num2= None
print(num1 , num2)
def register(request):
	global num1,num2
	if num1 is None and num2 is None:
		num1= random.randint(1,20)
		num2= random.randint(1,10)
		print(num1 , num2)

	if request.method == 'POST':
		sum1= num1+num2
		
		f_name= request.POST.get('first_name')
		username= request.POST.get('username')
		email= request.POST.get('Email')
		password1= request.POST.get('pass1')
		password2= request.POST.get('pass2')
		cap= int(request.POST.get('captcha'))
		print(cap)
		num1=None
		num2=None
		print(num1,num2)
		
		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'User already exists')
				return redirect ('registers')

			elif User.objects.filter(email= email).exists():
				messages.info(request, 'email already exists')
				return redirect('registers')

			elif cap != sum1:
				messages.info(request, 'Captcha Not Matched')
				return redirect('registers')


			else:
				user= User.objects.create_user(username=username , first_name= f_name , email= email, password=password1)
				user.save()
				
				print('user data created')
				return redirect('login')
		else:
			messages.info(request, 'password not maching')
			print('password not matching')
		return redirect('registers')
		
	return render(request , 'register.html',{'num1':num1, 'num2':num2})
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['pass1']
		user = auth.authenticate(username=username, password=password)

		if (user is not None) and (password == password):
			auth.login(request,user)
			return redirect('/')

		else:
			messages.info(request,'invalid credentials')
			return redirect('login')


	else:
		return render(request, 'login.html')


def logout(request):
	auth.logout(request)
	return redirect('/')

# def delete_post()