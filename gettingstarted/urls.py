from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ashley-table/$', hello.views.AshleyTableProcess.as_view(), name='ashley-table'),
    url(r'^global-u/$', hello.views.GlobalUInitialProcess.as_view(), name='global-u'),
    url(r'^coaster/$', hello.views.CoasterExcel.as_view(), name='coaster'),
    url(r'^coaster-p/$', hello.views.CoasterProcess.as_view(), name='coaster-process'),
)
