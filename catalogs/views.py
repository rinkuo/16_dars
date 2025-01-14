from django.shortcuts import render, redirect
from .models import Category


def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        parent_category = request.POST.get(
            'parent-category')

        if name and description:
            category = Category.objects.create(name=name, description=description)
            if parent_category:
                parent_category_obj = Category.objects.get(
                    id=parent_category)
                category.parent_category = parent_category_obj
                category.save()

            return redirect('home')
    return render(request, 'products/category-create.html')
