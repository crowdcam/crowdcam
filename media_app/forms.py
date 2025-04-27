from django import forms
from .models import Media
from django.core.exceptions import ValidationError

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

    # different clean, this one checks file types.
    def clean_file_field(self):
        ALLOWED_FILES = ["image/jpeg", "image/jpg", "image/gif", "image/png", "image/webp"]
        files = self.cleaned_data["file_field"]
        for file in files:
            if file.content_type not in ALLOWED_FILES:
                raise ValidationError(f"{file.name} is not a supported image type.")
        return files

class MediaReview(forms.ModelForm):
    class Meta:
        model = Media
        fields = ["status"]
        widgets = {
            "status": forms.Select(choices=(
                (None, "Awaiting Review"),
                (True, "Accepted"),
                (False, "Rejected")),
            )
        }
        edit_only = True