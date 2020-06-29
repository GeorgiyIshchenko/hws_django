from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone, dateformat

from .forms import *
from .models import *
from .serialiser import *

def tasks(request):
	if check_auth(request)==False:
		return redirect('/sign_in')
	user=request.user
	articles=Article.objects.filter(author=user)
	data_sorted=[]
	for i in articles:
		data_sorted.insert(0,i)
	return render(request,'tasks.html',context={"data":data_sorted,'user':user})

def homepage(request):
	if check_auth(request)==False:
		return redirect('/sign_in')
	user=request.user
	articles=Article.objects.filter(author=user)
	subject_names=[]
	for i in articles:
		if i.title not in subject_names:
			subject_names.append(i.title) 
	return render(request,'homepage.html',context={'subject_names':subject_names,'user':user})

def tasks_by_name(request,subject_name):
	if check_auth(request)==False:
		return redirect('/sign_in')
	user=request.user
	articles=Article.objects.filter(author=user)
	subject_articles=[]
	for i in articles:
		if i.title==subject_name:
			subject_articles.insert(0,i)
	return render(request,'subject_tasks.html',context={'data':subject_articles,'subject_name':subject_name,'user':user})

def task_extended(request,pk): 
	if check_auth(request)==False:
		return redirect('/sign_in')
	user=request.user
	article=Article.objects.get(pk=pk)
	time=dateformat.format(article.published_date,'Y.m.d')
	acces=False
	if user==article.author:
		acces=True
	return render(request,"task_extended.html",context={'article':article,'user':user,'acces':acces,'date':time})

def add_task(request):
	if check_auth(request)==False:
		return redirect('/sign_in')
	if request.method=='POST':
		form=PostForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.author = request.user
			task.published_date = timezone.now()
			task.save()
			return redirect('/tasks/'+str(task.pk))
	else:
		user=request.user
		form=PostForm()
	return render(request,'add_task.html',{'form':form,'user':user})

def edit_task(request,pk):
    if check_auth(request)==False:
        return redirect('/sign_in')
    task = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.published_date = timezone.now()
            task.save()
            return redirect('/tasks/'+str(task.pk))
    else:
        user=request.user
        form = PostForm(instance=task)
    return render(request, 'edit_task.html', {'form': form,'task':task})

def sign_in(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/')
    return render(request,'sign_in.html')

def sign_up(request):
	if request.method=='POST':
		users=User.objects.all()
		for i in users:
			if i.username==request.POST['username']:
				return render(request,'sign_up.html',{'username_exist':True})
		user=User.objects.create_user(username=request.POST['username'],
			email=request.POST['email'],
			password=request.POST['password'])
		user.save()
		return redirect('/sign_in')
	return render(request,'sign_up.html',{'username_exist':False})


def check_auth(request):
	if (not request.user.is_authenticated):
		print('Not ok')
		return False
	else:
		print('Ok')	

def logout(request):
	auth.logout(request)
	return redirect("/sign_in")



class TasksView(APIView):
	def get(self,request):
		articles=Article.objects.all()
		serialiser=ArticleSerializer(articles, many=True)
		return Response({'articles':serialiser.data})
	def post(self, request):
		article=request.data.get('article')
		serializer=ArticleSerializer(data=article)
		if serializer.is_valid(raise_exception=True):
			article_saved=serializer.save()
		return Response({"success": "Article '{}' created successfully".format(article_saved.pk)})
	def put(self, request, pk):
		saved_article = get_object_or_404(Article.objects.all(), pk=pk)
		data = request.data.get('article')
		serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
		if serializer.is_valid(raise_exception=True):
			article_saved = serializer.save()
		return Response({
			"success": "Article '{}' updated successfully".format(article_saved.pk)
		})
	def delete(self, request, pk):
		article = get_object_or_404(Article.objects.all(), pk=pk)
		article.delete()
		return Response({
		"message": "Article with id `{}` has been deleted.".format(pk)
		}, status=204)	

class UserView(APIView):
	def get(self,request):
		users=User.objects.all()
		serialiser=UserSerializer(users, many=True)
		return Response({'users':serialiser.data})
	def post(self, request):
		user=request.data.get('user')
		serializer=UserSerializer(data=user)
		if serializer.is_valid(raise_exception=True):
			user_saved=serializer.save()
		return Response({"success": "User '{}' created successfully".format(user_saved.pk)})
	def put(self, request, pk):
		saved_user = get_object_or_404(User.objects.all(), pk=pk)
		data = request.data.get('user')
		serializer = UserSerializer(instance=saved_user, data=data, partial=True)
		if serializer.is_valid(raise_exception=True):
			user_saved = serializer.save()
		return Response({
			"success": "User '{}' updated successfully".format(user_saved.pk)
		})
	def delete(self, request, pk):
		user = get_object_or_404(User.objects.all(), pk=pk)
		user.delete()
		return Response({
		"message": "User with id `{}` has been deleted.".format(pk)
		}, status=204)	
		