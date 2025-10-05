from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Photo, ClientProfile, Gallery, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'photo_count']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'date_taken', 'is_hero', 'is_featured', 'is_public', 'image_preview']
    list_filter = ['category', 'is_hero', 'is_featured', 'is_public', 'date_taken']
    list_editable = ['is_hero', 'is_featured', 'is_public']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date_uploaded'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.get_thumbnail_url())
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'session_date', 'phone', 'is_active', 'gallery_count']
    list_filter = ['session_type', 'session_date', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone']

    def gallery_count(self, obj):
        return obj.galleries.count()
    gallery_count.short_description = 'Galleries'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'photo_count', 'created_date', 'is_active', 'password_protected']
    list_filter = ['is_active', 'password_protected', 'created_date']
    search_fields = ['name', 'client__user__first_name', 'client__user__last_name']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['photos']

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project_type', 'created_date', 'is_read']
    list_filter = ['project_type', 'is_read', 'created_date']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_date']
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"