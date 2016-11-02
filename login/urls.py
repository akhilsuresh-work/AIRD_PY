

from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^airdlogin/$', views.airdlogin, name='airdlogin'),
    url(r'^airdlogout/$', views.airdlogout, name='airdlogout'),
    url(r'^(?P<question_id>[0-9]+)/detail$', views.detail, name='detail'),
    # ex: /login/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /login/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]