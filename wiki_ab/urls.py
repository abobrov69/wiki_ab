from django.conf.urls import patterns, include, url
from views import AboutView, display_meta

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wiki_ab.views.home', name='home'),
    # url(r'^wiki_ab/', include('wiki_ab.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^about/$', AboutView.as_view()),
    ('(^([^/]+)/([^/]+)/)*$', AboutView.as_view()),
)
