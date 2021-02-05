from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404,redirect


class ErrorMessageMiddleware(object):
	def __init__(self,get_response):
		self.get_response=get_response

	def __call__(self, request):
		response= self.get_response(request)
		return response

	def process_exception(self,exception,request):
		
		return redirect('registers')