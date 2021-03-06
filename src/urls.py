from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'neji.views.index', name='home'),
    url(r'^about.html$', 'django.views.generic.simple.direct_to_template', {'template': "markdown.html", "extra_context": {"markdown_src": "markdown/about.md"}}),
    url(r'^python.html$', 'django.views.generic.simple.direct_to_template', {'template': "markdown.html", "extra_context": {"markdown_src": "markdown/python.md"}}),
    url(r'^runpython$', 'neji.views.runpython'),
    url(r'^save', 'neji.views.save'),
    url(r'^new', 'neji.views.new'),
    url(r'^session/(?P<session_id>[a-f0-9]{32})/$', 'neji.views.code_session_page', name='session'),
    # url(r'^src/', include('src.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
