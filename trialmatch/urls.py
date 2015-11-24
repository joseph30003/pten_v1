from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.trial_list, name='trial_list'),
    url(r'search/$', views.search,name="search"),
    url(r'trialpage/$',views.trialpage,name="trialpage"),
]