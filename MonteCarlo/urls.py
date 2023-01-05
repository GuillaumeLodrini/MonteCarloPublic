"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import django.views.defaults
import MonteCarlo.celery

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from MonteCarlo.admin import admin_site


urlpatterns = [
    # Main
    path('', include('main.urls')),

    # User
    path('', include('user.urls')),

    # CMS
    path('api/cms/', include('cms.urls_api')),

    # Django Admin
    path('gdfcm/admin/', admin_site.urls),

    # Celery Progress Bars
    path('celery/progress/<uuid:task_id>/', MonteCarlo.celery.celery_progress, name='celery_progress'),
    path('celery/download/<uuid:task_id>/', MonteCarlo.celery.celery_download, name='celery_download')
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
       path('__debug__/', include(debug_toolbar.urls)),
    ]

    # Add media even debug is true
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add static even debug is true
    urlpatterns += staticfiles_urlpatterns()

    # While debug is true we still want to view our default/custom error page, otherwise we do not
    # know how they look like.
    def custom_page_not_found(request):
        """404 error page, returns the default page not found view."""

        return django.views.defaults.page_not_found(request, None)

    def custom_page_permission_denied(request):
        """403 error page, returns the default permission denied view."""

        return django.views.defaults.permission_denied(request, None)

    urlpatterns += [
        path('404/', custom_page_not_found),
        path('403/', custom_page_permission_denied),
    ]
