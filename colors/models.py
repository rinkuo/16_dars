from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=200)
    hex_code = models.CharField(max_length=200)

    def __str__(self):
        return self.name
