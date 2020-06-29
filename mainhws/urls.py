from django.urls import path

from .views import *

app_name="tasks"

urlpatterns = [
	path('tasks',tasks),
	path('',homepage),
	path('sign_in',sign_in),
	path('sign_up',sign_up),
	path('accounts/logout/', logout),
	path('add_task',add_task),
	path('tasks/<int:pk>/edit',edit_task),
	path('<str:subject_name>',tasks_by_name),
	path('tasks/<int:pk>',task_extended,name='taskcontent_url'),
	path('api/tasks',TasksView.as_view()),
	path('api/tasks/<int:pk>', TasksView.as_view()),
	path('api/users',UserView.as_view()),
	path('api/users/<int:pk>', UserView.as_view())
]