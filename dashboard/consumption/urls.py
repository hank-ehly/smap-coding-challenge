from django.conf.urls import url
from . import views

app_name = 'consumption'

urlpatterns = [
    url(r'^$', views.SummaryView.as_view(), name='summary'),
    url(r'^summary/$', views.SummaryView.as_view(), name='summary'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^api/v1/consumptions$', views.consumptions, name='consumptions'),
    url(r'^api/v1/consumptions/(?P<user_id>[0-9]+)$', views.user_consumptions, name='user_consumptions')
]
