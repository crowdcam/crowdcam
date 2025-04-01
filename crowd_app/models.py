from django.db import models
import os

# Create your models here.
class Media(models.Model):
    
    # TODO: when we get media storage going, set this up
    # media_path = models.FilePathField()
    media_path = models.CharField(max_length=200)
    user_id = models.IntegerField()
    organization_id = models.IntegerField()
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.media_path