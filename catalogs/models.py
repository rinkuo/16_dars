from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

    def __str__(self):
        return self.name
