from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from PIL import Image as PilImage
from .forms import ImageForm
from .models import UploadedImage
import io

def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            image = PilImage.open(uploaded_image.image)
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            if uploaded_image.aspect_ratio_locked:
                aspect_ratio = image.width / image.height
                height = int(width / aspect_ratio)
            resized_image = image.resize((width, height))
            
            resized_image_io = io.BytesIO()
            resized_image.save(resized_image_io, format='PNG')
            resized_image_file = default_storage.save(f'resized_images/{uploaded_image.image.name}.png', io.BytesIO(resized_image_io.getvalue()))
            
            uploaded_image.resized_image = resized_image_file
            uploaded_image.save()
            
            return redirect('preview_image', image_id=uploaded_image.id)
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import os

def preview_image(request, image_id):
    image = UploadedImage.objects.get(pk=image_id)
    if image.resized_image:
        file_path = os.path.join(settings.MEDIA_ROOT, image.resized_image.name)
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        return response
    return render(request, 'preview.html', {'image': image})
