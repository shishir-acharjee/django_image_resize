from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    resized_image = models.ImageField(upload_to='resized_images/', blank=True, null=True)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    aspect_ratio_locked = models.BooleanField(default=False)
