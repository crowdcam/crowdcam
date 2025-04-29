from django.db import models
from django.utils.text import slugify

class Organization(models.Model):
    name = models.CharField(max_length=255)
    join_code = models.CharField(max_length=20, null=True)
    accepting_users = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        app_label = 'organization'
        permissions = (
            ("user", "Member of org"),
            ("mod", "Moderator of org"),
            ("admin", "Admin of org")
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    def get_user_group(self):
        return self.name + "_user"

    def get_mod_group(self):
        return self.name + "_mod"

    def get_admin_group(self):
        return self.name + "_admin"

class MediaFile(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='organization_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)