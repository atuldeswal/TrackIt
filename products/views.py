from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Products, PriceUpdate
from datetime import date
from .utils import flipkart_scrapper, ebay_scrapper

User = get_user_model()

# View function for handling the dashboard page
@login_required(login_url='/entry/')
def dashboard(request):
    # Handling form submissions on the dashboard
    if request.method == 'POST':
        # Adding a product through the search form
        if 'search' in request.POST:
            product_url = request.POST.get('search')
            # Checking if the product already exists for the user
            existing_product = Products.objects.filter(product_url=product_url).first()
            if existing_product:
                # Informing the user if the product is already in their cart
                if existing_product.user.filter(id=request.user.id).exists():
                    messages.info(request, "Product present in your cart!")
                else:
                    # Adding the product to the user's cart if it's not already there
                    existing_product.user.add(request.user)
                    messages.success(request, 'Product added in your cart!')
                return redirect('dashboard')
            else:
                # Differentiating between Flipkart and eBay for scraping
                if product_url.startswith("https://www.flipkart.com/"):
                    product = flipkart_scrapper(product_url)
                elif product_url.startswith("https://www.ebay.com/"):
                    product = ebay_scrapper(product_url)
                else:
                    product = None  # Adding a fallback case for unsupported URLs
                
                # Validating and adding the new product to the database
                if product and 'error' not in product:
                    new_product = Products.objects.create(
                        product_url=product_url,
                        product_name=product['title'],
                        product_img=product['img_link'],
                        product_price=product['price'],
                        date_added=date.today()
                    )
                    print(product)
                    new_product.user.add(request.user)
                    # Creating a record for the initial price update
                    PriceUpdate.objects.create(product=new_product, price=product['price'], dates=date.today())
                    messages.success(request, 'Product added in your cart!')
                else:
                    # Handling failed product fetch attempts
                    messages.error(request, "Can't fetch details!")
                return redirect('dashboard')
        
        # Removing a product from the user's cart
        if 'remove_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = Products.objects.get(id=product_id)
            product.user.remove(request.user)
            return redirect('dashboard')
        
        # Logging out the user
        if 'lg' in request.POST:
            logout(request)
            return redirect('entry')

    # Preparing product data for display on the dashboard
    product_display = {}
    user_products = request.user.products_set.all()
    for product in user_products:
        price_updates = product.priceupdate_set.all()
        product_display[product.id] = {
            'product_id': product.id,
            'product_name': product.product_name,
            'product_url': product.product_url,
            'product_image': product.product_img,
            'product_price': product.product_price,
            'date_added': product.date_added,
            'all_price': [update.price for update in price_updates],
            'all_dates': [str(update.dates) for update in price_updates],
        }

    # Rendering the dashboard with the user's products
    return render(request, 'dashboard.html', {'products_info': product_display})
