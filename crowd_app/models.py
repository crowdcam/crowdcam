from django.db import models

class Tag(models.Model):
    #TODO validate field length
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name