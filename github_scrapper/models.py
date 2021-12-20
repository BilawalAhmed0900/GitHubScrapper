from django.db import models


# Create your models here.
class ScrappedUser(models.Model):
    username = models.TextField()
    location = models.TextField()
    email = models.TextField()
