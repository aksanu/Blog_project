"""blogpro2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.list_display , name='list_display'),
    path('tag/<tag_slug>', views.list_display , name='tagged'),
    path('<int:year>/<int:month>/<post>', views.detail_display , name='detail_display'),
    path('email-share/<int:id>', views.send_email , name='email'),
    path('create-post', views.CreatePost , name='create-post'),
    path('register', views.register , name='registers'),
    path('login', views.login , name='login'),
    path('logout', views.logout , name='logout'),
]
