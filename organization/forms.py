from django import forms
from .models import Organization
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Organization.objects.filter(name=name).exists():
            # check to make sure name is unique
            raise ValidationError(f"The name '{name}' is already taken.")
        return name

class JoinCodeForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["join_code", "accepting_users"]
        edit_only = True

class JoinCodeSubmit(forms.Form):
    input_code = forms.CharField(label="Join Code", max_length=20)

class UpdateUser(forms.Form):
    choices = [
        ('none', "DELETE USER"),
        ('user',"User Permissions"),
        ('mod', "Moderator Permissions"),
        ('admin', "Admin Permissions")
    ]
    permissions = forms.ChoiceField(choices=choices, required=True)