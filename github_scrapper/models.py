from django.db import models


# Create your models here.
class ScrappedUser(models.Model):
    username = models.TextField()
    fullname = models.TextField()
    notes = models.TextField()
