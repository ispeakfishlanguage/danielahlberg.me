from django.urls import path
from . import views
from . import views_seo
from . import views_verification

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.client_login, name='login'),
    path('logout/', views.client_logout, name='logout'),
    path('gallery/', views.client_gallery, name='client_gallery'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery_detail'),
    path('api/filter-photos/', views.filter_photos, name='filter_photos'),
    path('dashboard/', views.photographer_dashboard, name='photographer_dashboard'),
    path('gallery/<int:gallery_id>/photo/<int:photo_id>/toggle/', views.toggle_photo_selection, name='toggle_photo_selection'),

    # SEO files
    path('robots.txt', views_seo.robots_txt, name='robots_txt'),
    path('.well-known/security.txt', views_seo.security_txt, name='security_txt'),
    path('ads.txt', views_seo.ads_txt, name='ads_txt'),

    # Search engine verification files
    path('google<str:verification_code>.html', views_verification.google_site_verification, name='google_verification'),
    path('BingSiteAuth.xml', views_verification.bing_site_verification, name='bing_verification'),
    path('yandex_<str:verification_code>.html', views_verification.yandex_verification, name='yandex_verification'),
]