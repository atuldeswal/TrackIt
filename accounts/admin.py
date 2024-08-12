from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user_accounts
from products.models import Products

# Defines how products are displayed as inline objects in the User admin. This can be either Tabular or Stacked.
class ProductsInline(admin.TabularInline):  # admin.StackedInline for a different visual layout
    model = Products.user.through  # Specifies the intermediate model for a ManyToMany relationship
    extra = 1  # Default number of extra forms to display
    readonly_fields = ['product_info']  # Fields that are read-only in the admin

    def product_info(self, instance):
        # Custom method to display product information in a custom way
        return str(instance.product)  # Customize this based on your Products model fields
    
    product_info.short_description = 'Product Info'  # Sets a friendly name for the method in the admin

# Customizes the UserAdmin interface for our custom user model
class UserAccountsAdminList(UserAdmin):
    model = user_accounts
    list_display = ('email', 'is_verified', 'is_staff', 'date_joined', 'is_active')  # Fields to display in the user list
    list_filter = ('is_verified', 'is_active', 'date_joined')  # Filters available on the side panel
    search_fields = ('email',)  # Fields to be searched
    ordering = ('email',)  # Default ordering
    inlines = [ProductsInline,]  # Include the ProductsInline defined above to show related products

    # Customizes the fields shown in the user edit/add page in the admin
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_verified', 'is_active')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Defines fields to be displayed on the create user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_verified', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    # Adjusts the form to cater to custom user model requirements, particularly not using a username
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        # Disable certain fields if the current user is not a superuser
        if not is_superuser:
            disabled_fields |= {'is_staff', 'is_superuser', 'groups', 'user_permissions'}

        # Apply the disabled property to the specified fields
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

# Registers the custom user model with the custom admin interface
admin.site.register(user_accounts, UserAccountsAdminList)