from django.db import models

class BlogsPost(models.Model):
    title = models.CharField(max_length = 150)
    body = models.TextField()
    timestamp = models.DateTimeField(null = True)
    timestamp_s = models.CharField(max_length = 1000,null = True)
class Exchange_record(models.Model):
    context = models.CharField(max_length = 1000)
    timestamp = models.DateTimeField(null = True)
    timestamp_s = models.CharField(max_length = 1000,null = True)

class Infect_source(models.Model):
    infect_id = models.CharField(max_length = 10)
    timestamp = models.DateTimeField(null = True)
# Create your models here.
