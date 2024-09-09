from django import forms
from .models import UploadedImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image', 'width', 'height', 'aspect_ratio_locked']
