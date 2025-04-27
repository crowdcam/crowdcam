from django.db import models
from django.contrib.auth.models import User
from pathlib import Path

def media_path_formatter(instance, filename):
    org = instance.organization.name.replace(" ", "_")
    user = instance.user.username
    return Path ('media') / org / user / 'images' / filename

# Create your models here.
class Media(models.Model):
    # Explicit ID is not needed as it is handled automatically
    
    media_path = models.FileField(upload_to=media_path_formatter)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    # by default set tag to none, and on delete set tag feild to null
    tag = models.ForeignKey('crowd_app.Tag', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=None, null=True)
    # use argurment auto new add to set the time the media was uploaded.
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.media_path)