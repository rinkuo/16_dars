from django.db import models
from colors.base_model import BaseModel


class Brand(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='brands/')

    def __str__(self):
        return self.name
