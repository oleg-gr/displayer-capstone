from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Capability(models.Model):
    """Specifies a description of a capability"""

    description = models.CharField(max_length=200)

    class Meta:
        db_table = "displayer_capability"
        verbose_name_plural = "capabilities"

    def __str__(self):
        return self.description



class Location(models.Model):
    """Specifies what location a display is at"""

    description = models.CharField(max_length=200)

    class Meta:
        db_table = "displayer_location"

    def __str__(self):
        return self.description



class Display(models.Model):
    """Specifies location and capabilities of a display
    Also acts as a user so it can access '*/display' to display its tasks"""

    user = models.OneToOneField(User, primary_key=True)
    location = models.ForeignKey(Location)
    capabilities = models.ManyToManyField(Capability)

    class Meta:
        db_table = "displayer_display"



class DisplayerUser(models.Model):
    """DisplayerUser extends django user to store data about user"""
    user = models.OneToOneField(User, primary_key=True)
    n_number = models.CharField(max_length=9)

    class Meta:
        db_table = "displayer_user"



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



class Schedule(models.Model):
    """Specifies scheduled tasks; user specifies who scheduled the task"""
    user = models.ForeignKey(User)
    # description of why the task needs to exist (optional)
    description = models.CharField(max_length=200)
    display = models.ForeignKey(Display)
    task = models.ForeignKey(Task)
    start = models.DateTimeField(default=timezone.now())
    end = models.DateTimeField(default=(timezone.now() + timedelta(days=1)))

    class Meta:
        db_table = "displayer_schedule"