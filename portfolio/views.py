from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Photo, Category, Gallery, ClientProfile
from .forms import ContactForm, ClientLoginForm, GalleryPasswordForm


def home(request):
    """Homepage with hero section and featured photos"""
    hero_photos = Photo.objects.filter(is_hero=True, is_public=True)[:5]
    featured_photos = Photo.objects.filter(is_featured=True, is_public=True)[:6]
    context = {
        'hero_photos': hero_photos,
        'featured_photos': featured_photos,
    }
    return render(request, 'portfolio/home.html', context)


def portfolio(request):
    """Public portfolio gallery with filtering"""
    categories = Category.objects.all()
    category_slug = request.GET.get('category')

    photos = Photo.objects.filter(is_public=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        photos = photos.filter(category=category)

    context = {
        'photos': photos,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'portfolio/portfolio.html', context)


def about(request):
    """About page"""
    return render(request, 'portfolio/about.html')


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
            return redirect('portfolio:contact')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'portfolio/contact.html', context)


def client_login(request):
    """Client login page"""
    if request.user.is_authenticated:
        return redirect('portfolio:client_gallery')

    if request.method == 'POST':
        form = ClientLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('portfolio:client_gallery')
        messages.error(request, 'Invalid username or password.')
    else:
        form = ClientLoginForm()

    context = {'form': form}
    return render(request, 'portfolio/login.html', context)


@login_required
def client_logout(request):
    """Client logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('portfolio:home')


@login_required
def client_gallery(request):
    """Client's private gallery dashboard"""
    try:
        client_profile = request.user.clientprofile
        galleries = client_profile.galleries.filter(is_active=True)
    except ClientProfile.DoesNotExist:
        messages.error(request, 'No client profile found. Please contact the photographer.')
        return redirect('portfolio:home')

    context = {
        'client_profile': client_profile,
        'galleries': galleries,
    }
    return render(request, 'portfolio/client_gallery.html', context)


@login_required
def gallery_detail(request, slug):
    """Individual gallery view for clients"""
    gallery = get_object_or_404(Gallery, slug=slug, is_active=True)

    # Check if user has access to this gallery
    if gallery.client.user != request.user:
        messages.error(request, 'You do not have access to this gallery.')
        return redirect('portfolio:client_gallery')

    # Handle password protection
    if gallery.password_protected:
        if request.method == 'POST':
            form = GalleryPasswordForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['password'] == gallery.access_password:
                    request.session[f'gallery_{gallery.id}_access'] = True
                else:
                    messages.error(request, 'Incorrect password.')
                    return render(request, 'portfolio/gallery_password.html', {'form': form, 'gallery': gallery})
        else:
            if not request.session.get(f'gallery_{gallery.id}_access'):
                form = GalleryPasswordForm()
                return render(request, 'portfolio/gallery_password.html', {'form': form, 'gallery': gallery})

    photos = gallery.photos.all()

    context = {
        'gallery': gallery,
        'photos': photos,
    }
    return render(request, 'portfolio/gallery_detail.html', context)


@require_POST
def filter_photos(request):
    """AJAX endpoint for filtering photos"""
    category_slug = request.POST.get('category')

    if category_slug and category_slug != 'all':
        photos = Photo.objects.filter(category__slug=category_slug, is_public=True)
    else:
        photos = Photo.objects.filter(is_public=True)

    photo_data = []
    for photo in photos:
        photo_data.append({
            'id': photo.id,
            'title': photo.title,
            'image_url': photo.image.url,
            'thumbnail_url': photo.thumbnail.url if photo.thumbnail else photo.image.url,
            'category': photo.category.slug,
            'description': photo.description,
            'location': photo.location,
        })

    return JsonResponse({'photos': photo_data})