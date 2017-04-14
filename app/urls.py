from django.conf.urls import url

from app import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^clear/$', views.ClearView.as_view(url='/'), name='clear'),
]
