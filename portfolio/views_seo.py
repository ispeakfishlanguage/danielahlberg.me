from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string


@require_GET
def robots_txt(request):
    """Generate robots.txt file"""
    content = render_to_string('seo/robots.txt', {
        'sitemap_url': request.build_absolute_uri('/sitemap.xml'),
    })
    return HttpResponse(content, content_type='text/plain')


@require_GET
def security_txt(request):
    """Generate security.txt file"""
    content = render_to_string('seo/security.txt', {
        'domain': request.get_host(),
    })
    return HttpResponse(content, content_type='text/plain')


@require_GET
def ads_txt(request):
    """Generate ads.txt file if needed"""
    content = "# No ads currently running on this site\n"
    return HttpResponse(content, content_type='text/plain')