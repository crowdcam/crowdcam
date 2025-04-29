from django import forms
from django.core.exceptions import ValidationError
from .models import Tag

# new class for multiple files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# override for differnt arg
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    # check files are clean
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return [single_file_clean(data, initial)]

# orginal media form, no calls multi media form
class MediaForm(forms.Form):
    file_field = MultipleFileField()

    new_tag_name = forms.CharField(
        max_length=50,
        required=False,
        label="Create a new tag (Optional)"
    )

    def __init__(self, *args, **kwargs):
        # pop organization from kwargs, or set org to none
        org = kwargs.pop('organization', None)
        # call form init
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.ModelMultipleChoiceField(
            queryset= Tag.objects.none(),
            widget= forms.CheckboxSelectMultiple,
            required= False,
        )
        # if org has value
        if org:
            # set tag field to all organizations tags
            self.fields['tags'].queryset = Tag.objects.filter(organization=org)

    # different clean, this one checks file types.
    def clean_file_field(self):
        ALLOWED_FILES = ["image/jpeg", "image/jpg", "image/gif", "image/png", "image/webp"]
        files = self.cleaned_data["file_field"]
        for file in files:
            if file.content_type not in ALLOWED_FILES:
                raise ValidationError(f"{file.name} is not a supported image type.")
        return files


class MediaTagForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Select Tags"
    )
    new_tag_name = forms.CharField(
        max_length=50,
        required=False,
        label="Add a New Tag"
    )

    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['tags'].queryset = Tag.objects.filter(organization=organization)