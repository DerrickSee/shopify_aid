from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^update-ashley/$', hello.views.UpdateAshley.as_view(), name='update-ashley'),
    url(r'^global-u/$', hello.views.GlobalUInitialProcess.as_view(), name='global-u'),
    url(r'^coaster/$', hello.views.CoasterExcel, name='coaster'),
    url(r'^coaster-p/$', hello.views.CoasterProcess.as_view(), name='coaster-process'),
    url(r'^coaster-price-csv/$', hello.views.CoasterPriceCSV, name='coaster-price-csv'),
    url(r'^coaster-update-shopify/$', hello.views.UpdateCoasterShopifyExport.as_view(), name='coaster-update-shopify'),
    url(r'^clean/$', hello.views.CleanShopify.as_view(), name='clean-shopify'),
    url(r'^users/$', hello.views.ExportUsers, name='export-users'),
)
