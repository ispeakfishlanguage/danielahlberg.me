from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Photo, Category


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['portfolio:home', 'portfolio:portfolio', 'portfolio:about', 'portfolio:contact', 'portfolio:login']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item == 'portfolio:home':
            return 1.0
        elif item == 'portfolio:portfolio':
            return 0.9
        elif item in ['portfolio:about', 'portfolio:contact']:
            return 0.7
        return 0.5


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        # Get the latest photo in this category
        latest_photo = obj.photos.filter(is_public=True).first()
        return latest_photo.date_uploaded if latest_photo else None

    def location(self, obj):
        return f"{reverse('portfolio:portfolio')}?category={obj.slug}"


class PhotoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.4

    def items(self):
        return Photo.objects.filter(is_public=True, is_featured=True)

    def lastmod(self, obj):
        return obj.date_uploaded

    def location(self, obj):
        # Since we don't have individual photo pages, link to portfolio with category
        return f"{reverse('portfolio:portfolio')}?category={obj.category.slug}"