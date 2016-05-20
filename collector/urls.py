from django.conf.urls import url
from . import views

app_name = "collector"
urlpatterns = [
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list_tweets, name='list'),
    url(r'^filter/$', views.filter, name='filter'),
    url(r'^instructions/$', views.instructions, name='instructions'),
    url(r'^tweet/$', views.tweet_for_vote, name='tweet_vote'),
    url(r'^map/$', views.geo, name='map'),
    url(r'^(?P<tweet_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<tweet_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<tweet_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
