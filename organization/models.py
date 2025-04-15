from django.db import models

# Create your models here.
class Organization(models.Model):
    #TODO validate field length
    name = models.CharField(max_length=255)
    join_code = models.CharField(max_length=20, null=True)
    accepting_users = models.BooleanField(default=False)


    class Meta:
        permissions = (
            ("user", "Member of org"),
            ("mod", "Moderator of org"),
            ("admin", "Admin of org")
        )
    def __str__(self):
        return self.name

    def get_user_group(self):
        return self.name + "_user"

    def get_mod_group(self):
        return self.name + "_mod"

    def get_admin_group(self):
        return self.name + "_admin"