#Django's models.py file is primarily used to define tables in a database. Here’s a brief overview of how this works
    #Model Definition: Each model in models.py is a Python class that corresponds to a database table. The attributes of the class represent the columns of that table. For example, if you create a model named Member, it will create a table with fields like firstname and lastname in the database
    #Database Operations: When you define models, Django provides an Object-Relational Mapping (ORM) system that allows you to interact with the database using Python code instead of SQL. This means you can easily create, read, update, and delete records in the database through your model classes
    #Migrations: After defining or modifying models, you need to run migration commands (makemigrations and migrate). The makemigrations command generates the necessary SQL commands to create or update the tables based on your models, while the migrate command applies these changes to the actual database
#In summary, models.py serves as the blueprint for your database schema in a Django application, enabling efficient data management through well-defined models.    


# AbstractBaseUser: Describes the shape and behavior of your user.
# BaseUserManager: Controls how users are created and saved.
# They work together: The BaseUserManager uses the blueprint defined by AbstractBaseUser to manage the user lifecycle.

# Importing necessary Django modules for creating models and user management.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings

# UserManager class: This class is responsible for creating and managing user instances.
class UserManager(BaseUserManager):

    # Method to create a regular user with essential attributes.
    def create_user(self, first_name, last_name, username, email, password=None):
        # Check if the email is provided; if not, raise an error.
        if not email:
            raise ValueError("User must have an email address")
        
        # Check if the username is provided; if not, raise an error.
        if not username:
            raise ValueError("User must have a username")

        # Create a user instance using the provided information.
        user = self.model(
            email=self.normalize_email(email),  # Normalize the email format.
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        
        # Securely set the user's password.
        user.set_password(password)

        # Save the user instance to the database.
        user.save(using=self._db)

        return user  # Return the created user instance.
    
    # Method to create a superuser with elevated privileges.
    def create_superuser(self, first_name, last_name, username, email, password=None):
        # Create a regular user first.
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        # Set permissions and status flags for the superuser.
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_superuser = True
        # Save the superuser instance to the database.
        user.save(using=self._db)

        return user  # Return the superuser instance.



#the user model you defined in models.py is essential for managing user data and authentication in your Django application. It provides a structured way to store user information, facilitates user management, and integrates with Django's authentication system and admin interface.

# User class: This defines the structure of our custom User model.
class User(AbstractBaseUser, PermissionsMixin):

    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, "Restaurant"),
        (CUSTOMER, "Customer"),
    )

    # Defining fields for basic user information.
    first_name = models.CharField(max_length=50)  # First name of the user
    last_name = models.CharField(max_length=50)   # Last name of the user
    username = models.CharField(max_length=50, unique=True)  # Unique username
    email = models.EmailField(max_length=100, unique=True)  # Unique email address
    phone_number = models.CharField(max_length=12, blank=True)  # Optional phone number
    role = models.PositiveSmallIntegerField(choices= ROLE_CHOICE, blank=True, null = True)


    # Fields to track timestamps related to user activity.
    date_joined = models.DateTimeField(auto_now_add=True)  # Timestamp when the user joined
    last_login = models.DateTimeField(auto_now_add=True)   # Timestamp of last login
    modified_date = models.DateTimeField(auto_now_add=True)  # Timestamp of last modification
    created_date = models.DateTimeField(auto_now=True)      # Timestamp when record was created

    # Boolean fields for managing permissions and status of the user account.
    is_admin = models.BooleanField(default=False)  # Indicates if the user is an admin
    is_active = models.BooleanField(default=False)  # Indicates if the account is active
    is_superadmin = models.BooleanField(default=False)  # Indicates if the user has superadmin privileges
    is_staff = models.BooleanField(default=False)  # Indicates if the user can access admin features

    USERNAME_FIELD = "email"  # Specifies that users will log in using their email.

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]  # Additional required fields when creating a new user.

    objects = UserManager()  # Assigning our custom UserManager to manage User instances.

    def __str__(self):
        return self.email  # When printing a User object, display their email.

    def has_perms(self, perms, obj=None):
        return self.is_admin or self.is_superadmin or self.is_staff # Check if the user has admin or superadmin permissions.

    def has_module_perms(self, app_label):
        return self.is_staff or self.is_admin or self.is_superadmin  # Check access permissions for different modules.


# UserProfile class: This model stores additional information about users.
class UserProfile(models.Model):
    # Establishing a one-to-one relationship with the User model.
    # Each user can have one profile, and if the user is deleted, the profile will also be deleted.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    # Field for storing the user's profile picture.
    # The image will be uploaded to the specified directory.
    profile_picture = models.ImageField(upload_to="users/profile_pictures", blank=True, null=True)

    # Field for storing a cover photo for the user's profile.
    # The image will be uploaded to the specified directory.
    cover_photo = models.ImageField(upload_to="users/cover_photo", blank=True, null=True)

    # Address fields to store the user's location details.
    address_line1 = models.CharField(max_length=50, blank=True, null=True)  # First line of the address
    address_line2 = models.CharField(max_length=50, blank=True, null=True)  # Second line of the address (optional)
    
    # Fields for storing location details like country, state, city, and pin code.
    country = models.CharField(max_length=15, blank=True, null=True)  # Country name
    state = models.CharField(max_length=15, blank=True, null=True)    # State name
    city = models.CharField(max_length=15, blank=True, null=True)     # City name
    pin_code = models.CharField(max_length=6, blank=True, null=True)   # Postal code

    # Fields for storing geographical coordinates (latitude and longitude).
    latitude = models.CharField(max_length=20, blank=True, null=True)  # Latitude value
    longitude = models.CharField(max_length=20, blank=True, null=True)  # Longitude value

    # Timestamps for tracking when the profile was created and last modified.
    created_at = models.DateTimeField(auto_now_add=True)   # Automatically set when the profile is created
    modified_at = models.DateTimeField(auto_now=True)       # Automatically set when the profile is modified

    def __str__(self):
        return self.user.email  # Return the user's email for easy identification in admin or queries