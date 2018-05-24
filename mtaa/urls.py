from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from mtaa import views as core_views

urlpatterns = [
    url('^$', views.index, name='homepage'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent,
        name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^new/post$', views.new_post, name='post'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^profile/(?P<profile_id>[-\w]+)/$', views.profile, name='profile'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
