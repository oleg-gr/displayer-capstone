from django.contrib import admin

from ui.models import Capability

class CapabilityAdmin(admin.ModelAdmin):
    list_display = ('description', 'displays_list')
    search_fields = ['description', 'display__user__username']
    list_filter = ['display__user__username']

admin.site.register(Capability, CapabilityAdmin)

from ui.models import Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'displays_list')
    list_filter = ['name']
    search_fields = ['name', 'display__user__username']

admin.site.register(Location, LocationAdmin)

from ui.models import Display

class DisplayAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'capabilities_list_formatted')
    list_filter = ['location', 'capabilities']
    search_fields = ['user__username', 'location__name']

admin.site.register(Display, DisplayAdmin)

from ui.models import DisplayerUser

class DisplayerUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'n_number')
    search_fields = ['user__username', 'n_number']

admin.site.register(DisplayerUser, DisplayerUserAdmin)

from ui.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description', 'type')
    list_filter = ('user', 'type')
    search_fields = ['description']

admin.site.register(Task, TaskAdmin)


from ui.models import Schedule

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'start', 'end')
    # 'displays_list'
    # 'display__user__username'
    list_filter = ('user', 'task')
    search_fields = ['description']

admin.site.register(Schedule, ScheduleAdmin)

from ui.models import Media

class MediaAdmin(admin.ModelAdmin):
    list_display = ('media', 'task')
    list_filter = ('task',)
    search_fields = ['task']

admin.site.register(Media, MediaAdmin)