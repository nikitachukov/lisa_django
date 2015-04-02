from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lisa_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace="account")),
    url(r'^reports/', include('reports.urls', namespace="reports")),
    url(r'^$', 'reports.views.index', name='index'),
)
