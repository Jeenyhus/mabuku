from django.db import models

# Create your models here.

class Book (models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.ForeignKey('Genre', related_name='genre', on_delete=models.CASCADE)
    
class Genre (models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    