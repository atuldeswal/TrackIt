from django.contrib import admin
import threading
from django.http import HttpResponseRedirect
from .models import Products, PriceUpdate, TrackingStatus
from .price_update import update_all_products, get_most_recent_update_date

# Custom admin view for Products
class ProductAdminList(admin.ModelAdmin):  # Inherits from admin.ModelAdmin
    # Defines the columns that should be displayed in the admin list view
    list_display = ('product_name', 'product_price', "date_added")
    # Allows filtering of displayed products based on these fields
    list_filter = ('product_name', 'product_price', "date_added")
    # Enables a search box for these fields in the admin
    search_fields = ('product_name', 'product_price',)


# Custom admin view for PriceUpdate
class ProductPriceAdminList(admin.ModelAdmin):  # Inherits from admin.ModelAdmin
    list_display = ('get_product_name', 'dates', "price")

    def get_product_name(self, obj):
        # Custom method to display the name of the product related to a price update
        return obj.product.product_name
    get_product_name.short_description = 'Product Name'  # Column header for the custom field


@admin.register(TrackingStatus)
class TrackingStatusAdmin(admin.ModelAdmin):
    # Specifies a custom template to use for the change form of this model
    change_form_template = "admin/tracking_status_change_form.html"
    list_display = ('is_tracking',)  # Columns to display in the admin list view for TrackingStatus

    def response_change(self, request, obj):
        # Customizes the response after a change has been made to a TrackingStatus object
        if "start_tracking" in request.POST:
            # If the "start_tracking" button was pressed, start tracking
            obj.is_tracking = True
            obj.save()
            # Run the product update function in a separate thread to avoid blocking
            thread = threading.Thread(target=update_all_products)
            thread.daemon = True  # Allows thread to be killed when the main thread exits
            thread.start()
            self.message_user(request, "Tracking started.")
            return HttpResponseRedirect(".")
        elif "stop_tracking" in request.POST:
            # If the "stop_tracking" button was pressed, stop tracking
            obj.is_tracking = False
            obj.save()
            self.message_user(request, "Tracking stopped.")
            return HttpResponseRedirect(".")
        else:
            # If neither button was pressed, just proceed with the usual response
            return super().response_change(request, obj)

# Register the custom admin classes with their respective models
admin.site.register(Products, ProductAdminList)
admin.site.register(PriceUpdate, ProductPriceAdminList)
