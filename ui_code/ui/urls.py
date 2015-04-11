from django.conf.urls import patterns, include, url
from ui import views

urlpatterns = patterns('',
    # main redirector
    url(r'^$', views.index, name='index'),

    # display URL
    url(r'^display$', views.display, name='display'),
    # display API
    url(r'^display_heartbeat$', views.display_heartbeat, name='display_heartbeat'),
    url(r'^display_data$', views.display_data, name='display_data'),

    # user URL
    url(r'^manage$', views.manage, name='manage'),
    url(r'^tasks$', views.tasks, name='tasks'),
    url(r'^displays$', views.displays, name='displays'),
    url(r'^custom_task$', views.custom_task, name='custom_task'),
    # user API
    url(r'^displays_login_info$', views.displays_login_info, name='displays_login_info'),
    url(r'^schedules_active_info$', views.schedules_active_info, name='schedules_active_info'),
    # url(r'^upload_pic$', views.upload_pic, name='upload_pic'),
    url(r'^tasks/(?P<id>\d+)/info', views.schedule_task, name="info_task"),
    url(r'^tasks/(?P<id>\d+)/schedule', views.schedule_task, name="schedule_task"),
    url(r'^schedule$', views.schedule, name='schedule'),
)