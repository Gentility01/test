from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


# GO TO THE SETTINGS AND PUT IN THE SETTING FOR ABSTRACTUSERMODEL(line 30) this must be done also before makingmigrations BUT SET UP YOUR MODELS FIRST
# ALSO GO TO THE ADMIN.PY AND SET UP YOUR ADMINPAGE(DATABASE)


# CUSTOM USER MODEL MANAGER
#Django has built-in methods for the User Manager. We have to customize them in order to make our custom user model work correctly.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("user must have  an email address")
        
        if not username:
            raise ValueError("user must have a username")

        user = self.model(
             email=self.normalize_email(email), #this will make sure that the email will be in lowercase even if the user enters it with capital letters
             username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

#this one is for the superuser
    def create_superuser(self, email,username, password):
        user = self.create_user(
            email=self.normalize_email(email), #this will make sure that the email will be in lowercase even if the user enters it with capital letters
             username = username,
             password=password

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user





#SETTING UP WHERE THE PROFILE IMAGE WILL GO TO AND FORMATING THE NAME OF THE PROFILE IMAGE 
#the profile image will be saved in image_cdn  with the formated name and primary key 
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

#SETTING UP THE DEFULT PARTWAY
def get_default_profile_image():
    return "pictures/logo_1080_1080.png"

# uSER MODEL
class Acount(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email address",  max_length=255, unique=True,)
    username        = models.CharField(unique=True, max_length=50)
    date_joined     = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin        = models.BooleanField( default= False)
    is_active       = models.BooleanField( default= True)
    is_staff        = models.BooleanField( default= False)
    is_superuser    = models.BooleanField( default= False)
    profile_image   = models.ImageField( max_length=255, upload_to=get_profile_image_filepath, blank=True, null=True, default=get_default_profile_image)
    hide_email      = models.BooleanField(default=True)


    objects = MyAccountManager() #set the costomusermanager into our myaccountmanager


   


#HOW TO MAKE USER LOGIN WITH THEIR EMAIL INSTEAD OF USERNAME AND ADDING REQUIRED  FIELDS IN THE LOGIN PAGE
# the email assigned to the USERNAME_FIELD is from the email field in Acount model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username

#SETTING UP DEFAULT PERMISIONS THAT COMES WITH AbstractBaseUser
#here is a kinda default faunction to ask if the user have permission to do some stuffs if they are is_admin from the account model
    def has_perm(self, perm, obj=None):
        return self.is_admin
#here is ti check if the user have  module permission
    def has_module_perms(self, app_label):
        return True

#extracting the normal profile image name and replace it with profile_image.png (in line 9) and also the index
# goto ur app(account) create a file named backend.py  there to complete the changes
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email






    





