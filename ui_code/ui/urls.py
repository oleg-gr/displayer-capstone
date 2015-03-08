from django.conf.urls import patterns, include, url
from ui import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^manage$', views.manage, name='manage'),
   url(r'^display$', views.display, name='display'),
   url(r'^tasks$', views.tasks, name='tasks'),
   url(r'^displays$', views.displays, name='displays'),
   url(r'^custom_task$', views.custom_task, name='custom_task')
)