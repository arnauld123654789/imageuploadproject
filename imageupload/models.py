from django.db import models

class ImageModel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='imageformodel/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
