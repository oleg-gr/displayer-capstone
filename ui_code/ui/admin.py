from django.contrib import admin


from ui.models import Capability
admin.site.register(Capability)

from ui.models import Location
admin.site.register(Location)

from ui.models import Display
admin.site.register(Display)

from ui.models import DisplayerUser
admin.site.register(DisplayerUser)

from ui.models import Task
admin.site.register(Task)

from ui.models import Schedule
admin.site.register(Schedule)