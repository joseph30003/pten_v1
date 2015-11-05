from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.trial_list, name='trial_list'),
]