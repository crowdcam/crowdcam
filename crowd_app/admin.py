from django.contrib import admin
from .models import Media, Organization, Tag

# Every model must be registered in the admin.py
# file in order for it to be usable on the admin (dev) dashboard
admin.site.register(Media)
admin.site.register(Organization)
admin.site.register(Tag)
