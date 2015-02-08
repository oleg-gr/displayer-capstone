from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import collections
from datetime import datetime

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

    def capabilities_list(self):
        cap = self.capabilities.all()
        return "; ".join([x.description for x in cap])

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
    task = models.ForeignKey(Task)

    class Meta:
        db_table = "displayer_media"
        verbose_name_plural = "media"



class Schedule(models.Model):
    """Specifies scheduled tasks; user specifies who scheduled the task"""
    user = models.ForeignKey(User)
    # description of why the task needs to exist (optional)
    description = models.CharField(max_length=200)
    display = models.ForeignKey(Display)
    task = models.ForeignKey(Task)
    start = models.DateTimeField(default=timezone.now())
    end = models.DateTimeField(default=(timezone.now() + timedelta(days=1)))

    @classmethod
    def get_for_user(self, user):
        schedules = self.objects.filter(user=user)
        schedules_context = []
        for sh in schedules:
            d = collections.defaultdict(lambda: None)
            d['info'] = {
                'description': sh.description,
                'id': sh.id,
                'start': sh.start,
                'end': sh.end
                }
            d['display'] = {
                'name': sh.display.user,
                'id': sh.display.user.id
                }
            d['task'] = {
                'description': sh.task.description,
                'type': sh.task.type.description,
                'media': [
                        {
                            'id':file.id
                        } for file in Media.objects.filter(task=sh.task)
                    ]
                }
            schedules_context.append(d)
        return schedules_context

    class Meta:
        db_table = "displayer_schedule"