from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField('image', folder='portfolio/photos')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='photos')
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date_taken = models.DateField(null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_uploaded']

    def __str__(self):
        return self.title

    def get_thumbnail_url(self):
        """Generate thumbnail URL using Cloudinary transformations"""
        if self.image:
            return self.image.build_url(transformation=[
                {'width': 400, 'height': 400, 'crop': 'limit', 'quality': 'auto'}
            ])
        return None


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    session_date = models.DateField(null=True, blank=True)
    session_type = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.session_type}"


class Gallery(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='galleries')
    photos = models.ManyToManyField(Photo, related_name='galleries')
    cover_photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True, related_name='cover_for_galleries')
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    password_protected = models.BooleanField(default=False)
    access_password = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.name} - {self.client.user.get_full_name()}"

    def get_absolute_url(self):
        return reverse('portfolio:gallery_detail', kwargs={'slug': self.slug})


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    project_type = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.name} - {self.project_type}"