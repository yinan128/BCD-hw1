from django.db import models

# Create your models here.
from django.db.models import SET_NULL


class Facility(models.Model):
    # heating, ventilation, ac, lighting.
    category = models.CharField(max_length=20)

    name = models.CharField(max_length=50)

    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=20)

    manufacturer = models.CharField(max_length=20)
    dateInstalled = models.DateField()
    count = models.IntegerField(default=10)
    description = models.CharField(max_length=4000)


class AdditionalPicture(models.Model):
    content = models.FileField(blank=True)
    content_type = models.CharField(max_length=20)
    owner = models.ForeignKey(Facility, on_delete=SET_NULL, null=True)