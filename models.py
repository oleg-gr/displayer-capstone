from django.db import models

class Capability(models.Model):
    """Specifies a description of a capability"""

    description = models.CharField(max_length=200)

    class Meta:
        db_table = "displayer_capability"

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
    """Specifies location and capabilities of a display"""

    location = models.ForeignKey(Location)
    capabilities = models.ManyToManyField(Capability)

    class Meta:
        db_table = "displayer_display"