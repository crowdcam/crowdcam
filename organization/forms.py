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

class JoinCodeSubmit(forms.Form):
    input_code = forms.CharField(label="Join Code", max_length=20)