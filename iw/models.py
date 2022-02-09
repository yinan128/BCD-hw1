from django.db import models

# Create your models here.
from django.db.models import SET_NULL

class MainSys(models.Model):
    name = models.CharField(max_length=20)

    def __repr__(self):
        return "mainsys_" + self.name

class SubSys(models.Model):
    name = models.CharField(max_length=20)
    mainSys = models.ForeignKey(MainSys, on_delete=SET_NULL, null=True)

    def __repr__(self):
        return "subsys_" + self.name

class Facility(models.Model):
    subSys = models.ForeignKey(SubSys, on_delete=SET_NULL, null=True)

    # heating, ventilation, ac, lighting.
    category = models.CharField(max_length=20)

    name = models.CharField(max_length=50)

    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=20)

    manufacturer = models.CharField(max_length=20)
    dateInstalled = models.DateField()
    count = models.IntegerField(default=10)
    description = models.CharField(max_length=4000)

    def __repr__(self):
        return "facility_" + self.name


class AdditionalPicture(models.Model):
    content = models.FileField(blank=True)
    content_type = models.CharField(max_length=20)
    owner = models.ForeignKey(Facility, on_delete=SET_NULL, null=True)

class HistoricData(models.Model):
    label = models.CharField(max_length=30)
    category = models.CharField(max_length=20)
    filename = models.CharField(max_length=30)
    title = models.CharField(max_length=30, default="no name")

class SystemDiagram(models.Model):
    subSys = models.ForeignKey(SubSys, on_delete=SET_NULL, null=True)
    content = models.FileField(blank=True)
    content_type = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    init = models.BooleanField()

    def __repr__(self):
        return "sysDiagram_" + self.title