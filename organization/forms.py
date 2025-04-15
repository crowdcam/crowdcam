from django import forms
from .models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name"]

class JoinCodeForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["join_code", "accepting_users"]
        edit_only = True