from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('success/', views.success, name='success'),
    path('imageupload/image-list/', views.image_list, name='image_list'),
    path('index/', views.index, name='index'),
    path('pageDiagnostic/', views.pageDiagnostic, name='pageDiagnostic'),
    path('faireDiagnostic/', views.faireDiagnostic, name='faireDiagnostic'),
    path('ok/', views.ok, name='ok'),
]
