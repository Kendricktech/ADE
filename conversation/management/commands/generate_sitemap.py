import os
import importlib
from django.core.management.base import BaseCommand
from django.urls import URLPattern, URLResolver
from django.conf import settings

def extract_urls_from_patterns(patterns, parent_pattern=""):
    """
    Recursively extract all URL patterns from a Django URL resolver.
    """
    urls = []
    for pattern in patterns:
        if isinstance(pattern, URLPattern):  # Simple URL pattern
            full_pattern = parent_pattern + str(pattern.pattern)
            urls.append(full_pattern)
        elif isinstance(pattern, URLResolver):  # Nested URL resolver
            nested_pattern = parent_pattern + str(pattern.pattern)
            urls.extend(extract_urls_from_patterns(pattern.url_patterns, nested_pattern))
    return urls

def collect_urls_from_apps():
    """
    Collect all URLs defined in the project's `urls.py` files.
    """
    urlconf = importlib.import_module(settings.ROOT_URLCONF)
    patterns = urlconf.urlpatterns
    return extract_urls_from_patterns(patterns)

def generate_html_sitemap(urls, output_file):
    """
    Generate an HTML file for the sitemap.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Website Sitemap</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
            h1 { text-align: center; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 5px 0; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Website Sitemap</h1>
        <ul>
    """
    for url in urls:
        html_content += f'<li><a href="{url}">{url}</a></li>\n'

    html_content += """
        </ul>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

class Command(BaseCommand):
    help = "Generate an HTML sitemap from all the URLs defined in the project."

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='sitemap.html',
            help='The output file where the sitemap will be saved.'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        self.stdout.write(self.style.NOTICE("Collecting URLs from your project..."))
        urls = collect_urls_from_apps()
        urls = [url.lstrip('^').rstrip('$') for url in urls]  # Clean up regex characters
        self.stdout.write(self.style.SUCCESS(f"Found {len(urls)} URL(s)."))

        self.stdout.write(self.style.NOTICE(f"Generating sitemap HTML in {output_file}..."))
        generate_html_sitemap(urls, output_file)
        self.stdout.write(self.style.SUCCESS(f"Sitemap has been successfully saved to {output_file}."))
