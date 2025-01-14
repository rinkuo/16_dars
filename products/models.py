from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from brands.models import Brand
from catalogs.models import Category
from colors.models import Color

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('products:detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])

    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField(max_length=200)
    review = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
    )

    def __str__(self):
        return f"Review for {self.product.name} by {self.name}"

