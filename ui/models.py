from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
import collections
from datetime import datetime, date, timedelta
from jsonfield import JSONField

class Capability(models.Model):
    """Specifies a description of a capability"""

    description = models.CharField(max_length=200)

    class Meta:
        db_table = "displayer_capability"
        verbose_name_plural = "capabilities"

    def __str__(self):
        return self.description

    def displays_list(self):
        disp = Display.objects.filter(capabilities=self)
        return "; ".join([x.user.username for x in disp])



class Location(models.Model):
    """Specifies what location a display is at"""

    name = models.CharField(max_length=200)

    class Meta:
        db_table = "displayer_location"

    def __str__(self):
        return self.name

    def displays_list(self):
        disp = Display.objects.filter(location=self)
        return "; ".join([x.user.username for x in disp])


class Display(models.Model):
    """Specifies location and capabilities of a display
    Also acts as a user so it can access '*/display' to display its tasks"""

    user = models.OneToOneField(User, primary_key=True)
    location = models.ForeignKey(Location)
    capabilities = models.ManyToManyField(Capability)
    last_active = models.DateTimeField(default=datetime.now())

    @classmethod
    def get_data_for_display(self, display):
        to_display = Schedule.objects.filter(displays=display.display,
                start__lte=datetime.now(), end__gte=datetime.now())

        data = { 'tasks' : [] , 'id' : display.id}

        for schedule in to_display:
            options = schedule.options
            start = datetime.combine(schedule.start, datetime.min.time())
            start = start.replace(hour = options['time']['start'])
            end = schedule.end
            end = datetime.combine(end, datetime.min.time())
            hour = options['time']['end']
            if hour == 24:
                end += timedelta(days = 1)
            else:
                end = end.replace(hour = hour)
            now = datetime.now()
            print start
            print end
            if start > now or end < now:
                continue

            task = schedule.task
            type = task.type.id
            media = [x.media.url for x in Media.objects.filter(task=task)]
            if type == 5:
                data['tasks'] =   [{
                'type': type,
                'media': media,
                'options': options,
                'id': task.id
                }]
                return data
            data['tasks'].append({
                'type': type,
                'media': media,
                'options': options,
                'id': task.id
                })

        return data

    # TO-DO: rewrite this
    @classmethod
    def get_for_display(self, display):
        display = Schedule.objects.filter(display=display,
                start__lte=datetime.now(), end__gte=datetime.now())
        display_context = []
        for ds in display:
            d = collections.defaultdict(lambda: None)
            d['task'] = {
                'type': ds.task.type,
                'media': [file for file in Media.objects.filter(task=ds.task)]
                }
            display_context.append(d)
        return display_context

    @classmethod
    def get_basic_display_info(self):
        # Get basic info for listing displays
        all_displays = Display.objects.all().order_by('-last_active')
        list_of_displays = []
        for display in all_displays:
            display_entry = {
                'id' : display.user_id,
                'name': display.user.username,
                'location' : display.location.name,
                'capabilities': "<br>".join(display.capabilities_list())
            }
            list_of_displays.append(display_entry)
        return list_of_displays

    @classmethod
    def get_login_info(self):
        # Lists id's of displays and seconds since last active
        all_displays = Display.objects.all()
        list_of_displays_login_info = {}
        now = datetime.now()
        for display in all_displays:
            last_active = display.last_active
            list_of_displays_login_info[display.user_id] = (now - last_active).total_seconds()
        return list_of_displays_login_info

    def capabilities_list(self):
        # returns list of capabilities for a display
        all_capabilities = self.capabilities.all()
        return [capability.description for capability in all_capabilities]

    def capabilities_list_formatted(self):
        # returns list of capabilities for a display as a string
        # required for proper displaying of admin panel
        return "; ".join(self.capabilities_list())

    class Meta:
        db_table = "displayer_display"

    def __str__(self):
        return self.user.username



class DisplayerUser(models.Model):
    """DisplayerUser extends django user to store data about user"""
    user = models.OneToOneField(User, primary_key=True)
    n_number = models.CharField(max_length=9)

    class Meta:
        db_table = "displayer_user"

    def __str__(self):
        return self.user.username



class Task(models.Model):
    """Specifies reusable task; user specifies who created the task"""
    user = models.ForeignKey(User)
    description = models.CharField(max_length=200)
    # type of task (maps to capabilities)
    type = models.ForeignKey(Capability)
    # public tasks are visible to everyone
    public = models.BooleanField(default=False)

    class Meta:
        db_table = "displayer_task"

    def __str__(self):
        return self.description

class Media(models.Model):
    """Stores pictures, sounds, videos"""
    media = models.FileField()
    # can be empty (for previews and other things)
    task = models.ForeignKey(Task)
    uuid = models.CharField(max_length=64)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "displayer_media"
        verbose_name_plural = "media"



class Schedule(models.Model):
    """Specifies scheduled tasks; user specifies who scheduled the task"""
    user = models.ForeignKey(User)
    displays = models.ManyToManyField(Display)
    task = models.ForeignKey(Task)
    start = models.DateField(default=timezone.now())
    end = models.DateField(default=(timezone.now() + timedelta(days=1)))
    options = JSONField()

    # TO-DO: fill in displays (requires changing model and making groups
    # of displays)
    @classmethod
    def get_list_of_schedules(self, user):
        # Returns basic info about schedules
        all_schedules_for_user = self.objects.filter(user=user)
        schedules_info = []
        for schedule in all_schedules_for_user:
            displays = []
            disp_options = schedule.options["screens"]
            if disp_options["type"] == "individual":
                for display in Display.objects.filter(schedule=schedule):
                    displays.append(str(display))
                displays = "<br>".join(displays)
            else:
                if disp_options["value"] == "all":
                    displays = "All available displays"
                else:
                    displays = "Displays in " + disp_options["value"]
            d = {
                'id' : schedule.id,
                'description' : schedule.task.description,
                'displays' : displays,
                'task_type' : schedule.task.type.description,
                'task_id' : schedule.task.id
            }
            schedules_info.append(d)
        return schedules_info

    @classmethod
    def get_schedules_active_info(self, user):
        # Lists id's of displays and seconds since last active
        all_schedules_for_user = self.objects.filter(user=user)
        list_of_schedules = {}
        for schedule in all_schedules_for_user:
            start = schedule.start
            start = datetime.combine(start, datetime.min.time())

            options = schedule.options

            start = start.replace(hour = options['time']['start'])

            starts_in = (datetime.now() - start).total_seconds()

            if starts_in < 0:
                active = False
                list_of_schedules[schedule.id] = {
                    "time" : -starts_in,
                    "active" : active
                }
            else:
                active = True
                end = schedule.end
                end = datetime.combine(end, datetime.min.time())
                hour = options['time']['end']
                if hour == 24:
                    end += timedelta(days = 1)
                else:
                    end = end.replace(hour = hour)

                ends_in = (datetime.now() - end).total_seconds()

                list_of_schedules[schedule.id] = {
                    "time" : ends_in,
                    "active" : active
                }


        return list_of_schedules

    def displays_list(self):
        disp = Display.objects.filter(schedule=self)
        return "; ".join([x.user.username for x in disp])

    class Meta:
        db_table = "displayer_schedule"


# classes for forms
# class ImageUploadForm(forms.Form):
#     """Image upload form."""
#     image = forms.ImageField()
