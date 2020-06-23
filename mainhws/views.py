from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .models import *
from .serialiser import *

def tasks(request):
	data=Article.objects.all()
	data_sorted=[]
	for i in data:
		data_sorted.insert(0,i)
	return render(request,'tasks.html',context={"data":data_sorted})

def homepage(request):
	articles=Article.objects.all()
	subject_names=[]
	for i in articles:
		if i.title not in subject_names:
			subject_names.append(i.title) 
	return render(request,'homepage.html',context={'subject_names':subject_names})

def tasks_by_name(request,subject_name):
	articles=Article.objects.all()
	subject_articles=[]
	for i in articles:
		if i.title==subject_name:
			subject_articles.insert(0,i)
	return render(request,'subject_tasks.html',context={'data':subject_articles,'subject_name':subject_name})

def task_extended(request,slug): 
	article=Article.objects.get(slug=slug)
	return render(request,"task_extended.html",context={'article':article})

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
		return Response({"success": "Article '{}' created successfully".format(article_saved.slug)})
	def put(self, request, pk):
		saved_article = get_object_or_404(Article.objects.all(), pk=pk)
		data = request.data.get('article')
		serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
		if serializer.is_valid(raise_exception=True):
			article_saved = serializer.save()
		return Response({
			"success": "Article '{}' updated successfully".format(article_saved.slug)
		})
	def delete(self, request, pk):
		article = get_object_or_404(Article.objects.all(), pk=pk)
		article.delete()
		return Response({
		"message": "Article with id `{}` has been deleted.".format(pk)
		}, status=204)	
		