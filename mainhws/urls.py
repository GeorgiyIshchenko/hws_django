from django.urls import path

from .views import *

app_name="tasks"

urlpatterns = [
	path('tasks',tasks),
	path('',homepage),
	path('<str:subject_name>',tasks_by_name),
	path('tasks/<str:slug>',task_extended,name='postcontent_url'),
	path('api/tasks',TasksView.as_view()),
	path('api/tasks/<int:pk>', TasksView.as_view())
]