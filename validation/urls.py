from django.conf.urls import url
from . import views


urlpatterns = [
	url (r'^$', views.summaries, name='validation'),
	url (r'^(?P<scenarioID>[0-9]+)/$', views.querySummaries, name='query_validation'),
	url (r'^admin/$', views.admin, name='validation_admin'),
	url (r'^admin/(?P<queryID>[0-9]+)/$',views.queryLists,name='query_detail'),
	url (r'^trial/(?P<trialID>[0-9]+)/$', views.TrialValidation, name='trial_content'),

]