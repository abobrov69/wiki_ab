from django.conf.urls import patterns, include, url
from views import AboutView, WikiPageView, RootPageView, WikiPageUpdate, WikiPageDelete, WikiPageCreate, wiki_page_not_found

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()

handler404 = 'wiki_ab.views.wiki_page_not_found'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wiki_ab.views.home', name='home'),
    # url(r'^wiki_ab/', include('wiki_ab.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url('^$', RootPageView.as_view (), name="rootpage"),
    url(r'^admin/', include(admin.site.urls)),
    (r'^about/$', AboutView.as_view()),
#    (r'(^([^/]+)/)*(tst/|tst)$', wiki_page_not_found),
    (r'(^([^/]+)/)*(add/|add)$', WikiPageCreate.as_view()),
    (r'(^([^/]+)/)*(edit/|edit)$', WikiPageUpdate.as_view()),
    (r'(^([^/]+)/)*(delete/|delete)$', WikiPageDelete.as_view()),
    (r'(^([^/]+)/)*$', WikiPageView.as_view()),
)
