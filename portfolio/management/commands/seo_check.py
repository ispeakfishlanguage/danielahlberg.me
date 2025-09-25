from django.core.management.base import BaseCommand
from django.urls import reverse
from django.test import Client
from django.conf import settings
import requests
from urllib.parse import urljoin


class Command(BaseCommand):
    help = 'Check SEO configuration and submit sitemap to search engines'

    def add_arguments(self, parser):
        parser.add_argument(
            '--submit-sitemap',
            action='store_true',
            help='Submit sitemap to Google Search Console',
        )
        parser.add_argument(
            '--check-urls',
            action='store_true',
            help='Check if all important URLs are accessible',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting SEO Check...'))

        # Check important URLs
        if options['check_urls']:
            self.check_urls()

        # Check SEO files
        self.check_seo_files()

        # Check meta tags
        self.check_meta_tags()

        # Submit sitemap if requested
        if options['submit_sitemap']:
            self.submit_sitemap()

        self.stdout.write(self.style.SUCCESS('SEO Check completed!'))

    def check_urls(self):
        """Check if important URLs are accessible"""
        self.stdout.write('Checking URL accessibility...')

        client = Client()
        urls_to_check = [
            ('home', 'portfolio:home'),
            ('portfolio', 'portfolio:portfolio'),
            ('about', 'portfolio:about'),
            ('contact', 'portfolio:contact'),
            ('sitemap', None),  # Direct URL
            ('robots.txt', 'portfolio:robots_txt'),
        ]

        for name, url_name in urls_to_check:
            try:
                if url_name:
                    url = reverse(url_name)
                else:
                    url = '/sitemap.xml'

                response = client.get(url)
                if response.status_code == 200:
                    self.stdout.write(f'✅ {name}: OK ({url})')
                else:
                    self.stdout.write(
                        self.style.ERROR(f'❌ {name}: {response.status_code} ({url})')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ {name}: Error - {str(e)}')
                )

    def check_seo_files(self):
        """Check if SEO files are accessible"""
        self.stdout.write('Checking SEO files...')

        client = Client()
        seo_files = [
            ('robots.txt', 'portfolio:robots_txt'),
            ('sitemap.xml', None),
            ('security.txt', 'portfolio:security_txt'),
        ]

        for name, url_name in seo_files:
            try:
                if url_name:
                    url = reverse(url_name)
                else:
                    url = '/sitemap.xml'

                response = client.get(url)
                if response.status_code == 200:
                    self.stdout.write(f'✅ {name}: Accessible')
                    if 'xml' in name.lower():
                        # Check if XML is valid
                        if b'<?xml' in response.content:
                            self.stdout.write(f'  📄 {name}: Valid XML format')
                        else:
                            self.stdout.write(f'  ⚠️ {name}: May not be valid XML')
                else:
                    self.stdout.write(
                        self.style.ERROR(f'❌ {name}: Not accessible ({response.status_code})')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ {name}: Error - {str(e)}')
                )

    def check_meta_tags(self):
        """Check if meta tags are present on key pages"""
        self.stdout.write('Checking meta tags...')

        client = Client()
        pages_to_check = [
            ('Home', 'portfolio:home'),
            ('Portfolio', 'portfolio:portfolio'),
            ('About', 'portfolio:about'),
            ('Contact', 'portfolio:contact'),
        ]

        for page_name, url_name in pages_to_check:
            try:
                url = reverse(url_name)
                response = client.get(url)
                content = response.content.decode('utf-8')

                # Check for essential meta tags
                checks = [
                    ('Title tag', '<title>' in content),
                    ('Meta description', 'name="description"' in content),
                    ('Canonical URL', 'rel="canonical"' in content),
                    ('Open Graph', 'property="og:' in content),
                    ('Structured data', 'application/ld+json' in content),
                ]

                self.stdout.write(f'\n📄 {page_name} page:')
                for check_name, passed in checks:
                    status = '✅' if passed else '❌'
                    self.stdout.write(f'  {status} {check_name}')

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ {page_name}: Error - {str(e)}')
                )

    def submit_sitemap(self):
        """Submit sitemap to Google Search Console"""
        self.stdout.write('Submitting sitemap to search engines...')

        # Note: Automatic submission requires API keys
        # This is a placeholder for manual instruction
        self.stdout.write(
            self.style.WARNING(
                'Manual action required: Submit sitemap.xml to:\n'
                '1. Google Search Console: https://search.google.com/search-console/\n'
                '2. Bing Webmaster Tools: https://www.bing.com/webmasters/\n'
                '3. Sitemap URL: /sitemap.xml'
            )
        )