from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.conf import settings


@require_GET
def google_site_verification(request):
    """
    Google Search Console verification file
    Replace 'your-google-verification-code' with actual code from Google Search Console
    """
    verification_code = getattr(settings, 'GOOGLE_SITE_VERIFICATION', 'google-site-verification-placeholder')
    content = f"google-site-verification: {verification_code}.html"
    return HttpResponse(content, content_type='text/plain')


@require_GET
def bing_site_verification(request):
    """
    Bing Webmaster Tools verification file
    Replace with actual verification code from Bing Webmaster Tools
    """
    verification_code = getattr(settings, 'BING_SITE_VERIFICATION', 'bing-site-verification-placeholder')
    content = f'<?xml version="1.0"?>\n<users>\n    <user>{verification_code}</user>\n</users>'
    return HttpResponse(content, content_type='application/xml')


@require_GET
def yandex_verification(request):
    """Yandex verification file (optional for international SEO)"""
    verification_code = getattr(settings, 'YANDEX_VERIFICATION', 'yandex-verification-placeholder')
    content = f'<html><head><meta name="yandex-verification" content="{verification_code}" /></head><body></body></html>'
    return HttpResponse(content, content_type='text/html')