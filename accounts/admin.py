from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# CustomUserAdmin class: This class customizes how the User model appears in the admin interface.
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view of users.
    list_display = ("email", "username", "first_name", "last_name", "role")
    
    # Specifys which fields should be readonly
    readonly_fields = ("username", "email", "first_name", "last_name", "password")

    # These options are left empty to disable filtering and grouping.
    filter_horizontal = ()  
    list_filter = ()  
    # Define the layout of fields in the user edit form.
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password'),
        }),
    )
# Registering the User model with the custom admin class.
admin.site.register(User, CustomUserAdmin)  # This links the User model to the CustomUserAdmin configuration.

# Register the UserProfile model with the admin site
admin.site.register(UserProfile)