from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

# REMOVED: from . import views (This was looking in the wrong folder!)

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

# This is the correct import for your search views
from search import views as search_views

# Patterns that do NOT get a language prefix (Admin and Dev tools)
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("i18n/", include("django.conf.urls.i18n")),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Patterns that DO get a language prefix (e.g., /en/search/)
urlpatterns += i18n_patterns(
    path("search/", search_views.search, name="search"),
    
    # FIX: The API endpoint MUST go above the Wagtail catch-all!
    path('api/ai-summary/', search_views.ai_search_summary, name='ai_search_summary'),
    
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the very last item.
    path("", include(wagtail_urls)),
    
    # If True, the default language (English) will always show /en/ in the URL
    prefix_default_language=True,
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)