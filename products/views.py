from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Review
from decimal import Decimal
from brands.models import Brand
from catalogs.models import Category
from colors.models import Color


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category__id=category)
    ctx = {'products': products, 'categories': categories}
    return render(request, 'index.html', ctx)

def product_list(request):
    products = Product.objects.all()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sort = request.GET.get('sort', '')

    if min_price:
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = None
    if max_price:
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = None

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)

    if brands:
        products = products.filter(brand__id__in=brands)
    if colors:
        products = products.filter(color__id__in=colors)

    if sort == 'low_to_high':
        products = products.order_by('price')
    elif sort == 'high_to_low':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    ctx = {
        'products': products,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
        'selected_brands': [int(b) for b in brands],
        'selected_colors': [int(c) for c in colors],
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    }
    return render(request, 'products/product-by-category.html', ctx)


def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        color_id = request.POST.get('color')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if name and price and brand_id and category_id and color_id and description and image:
            try:
                price = Decimal(price)
                brand = Brand.objects.get(id=brand_id)
                category = Category.objects.get(id=category_id)
                color = Color.objects.get(id=color_id)

                Product.objects.create(
                    name=name,
                    price=price,
                    brand=brand,
                    category=category,
                    color=color,
                    description=description,
                    image=image,
                )
                return redirect('products:list')
            except (ObjectDoesNotExist, IntegrityError) as e:
                error_message = f"Error: {str(e)}"
        else:
            error_message = "All fields are required."
    else:
        error_message = None

    return render(request, 'products/product-create.html', {
        'error_message': error_message,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
    })


def product_detail(request, year, month, day, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day,
    )
    reviews = Review.objects.filter(product=product)

    star_range = range(1, 6)

    ctx = {'product': product, 'reviews': reviews, 'star_range': star_range}
    return render(request, 'products/product-detail.html', ctx)



def create_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        rating = int(request.POST.get('rating'))
        review_text = request.POST.get('review')

        if name and review_text:
            try:
                Review.objects.create(name=name, rating=rating, review=review_text, product=product)
                messages.success(request, "Review submitted successfully!")
                return redirect(product.get_detail_url())
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Please provide both name and review.")

    ctx = {'product': product, 'reviews': Review.objects.filter(product=product)}
    return render(request, 'products/review-create.html', ctx)
