from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    """We fork the admin class to customise it a little bit."""

    # Text to put at the end of each page's <title>.
    site_title = 'Admin site'

    # Text to put in each page's <h1> (and above login form).
    site_header = 'Admin site'

    # Text to put at the top of the admin index page.
    index_title = 'Admin'

    # URL where the "View site" button redirects to.
    site_url = '/'


# We register our custom admin, do not forget to include it into the urls.py instead of the standard django admin
admin_site = CustomAdminSite()

# Register Site application into our custom admin
# from django.contrib.sites.models import Site
# from django.contrib.sites.admin import SiteAdmin
# admin_site.register(Site, SiteAdmin)
