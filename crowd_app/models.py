from django.db import models
from django.contrib.auth import get_user_model
from organization.models import Organization

User = get_user_model()

class Tag(models.Model):
    #TODO validate field length
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Media(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="crowd_media")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crowd_user_media")
    media_path = models.FileField(upload_to='media_files/')  # example path
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_path.name} uploaded by {self.user.username}"