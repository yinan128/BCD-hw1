from django.db import models

# Create your models here.
class Facility(models.Model):
    # heating, ventilation, ac, lighting.
    category = models.CharField(max_length=20)

    name = models.CharField(max_length=50)

    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=20)
    description = models.CharField(max_length=20)

