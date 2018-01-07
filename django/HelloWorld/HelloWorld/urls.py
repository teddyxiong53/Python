from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import view, testdb, search, search2
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HelloWorld.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello$', view.hello),
    url(r'^testdb$', testdb.testdb),
    url(r'^getdb$', testdb.getdb),
    url(r'^updatedb$', testdb.updatedb),
    url(r'^deldb$', testdb.deldb),
	url(r'^search-form$',search.search_form),
	url(r'^search$', search.search),
	url(r'^search-post$', search2.search_post),
)
