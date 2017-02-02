from django.conf.urls import url
from pten import views

from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', views.Query_view, name='trialMatch_v2' ),
	url (r'^login/$', 'django.contrib.auth.views.login',
	     {
		     "template_name": "login.html",

	     },
	     name="login"),

	# Map the 'django.contrib.auth.views.logout' view to the /logout/ URL.
	# Pass additional parameters to the view like the page to show after logout
	# via a dictionary used as the 3rd argument.
	url (r'^logout/$', 'django.contrib.auth.views.logout',
	     {
		     "next_page": reverse_lazy ('login')
	     }, name="logout"),



]