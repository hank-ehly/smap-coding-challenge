from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SummaryView.as_view(), name='summary'),
    url(r'^summary/$', views.SummaryView.as_view(), name='summary'),
    url(r'^detail/', views.detail),

    url(r'^api/consumption_summary/$', views.consumption_summary)
]
