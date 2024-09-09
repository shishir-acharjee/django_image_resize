from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='home'),  # Add this line
    path('upload/', views.upload_image, name='upload_image'),
    path('preview/<int:image_id>/', views.preview_image, name='preview_image'),
]
