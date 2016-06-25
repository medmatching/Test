from django.conf.urls import include,url


from . import views
print ( url )


urlpatterns = [
    # /metric/
    url(r'^$', views.index, name='index'),
    
    # /metric/10016/
    #url(r'^(?P<zipcode>[0-9]{5})/$', views.detail, name='detail'),
    url(r'detail', views.detail, name='detail'),
]

