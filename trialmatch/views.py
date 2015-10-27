from django.http import HttpResponse
from django.template.loader import get_template
import datetime

def homepage(request):
    return HttpResponse("This is clinical trial matching website")

def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('time.html')
    html = t.render({'current_date':now,'name_list':["abhishek","talluri"]})
    return HttpResponse(html)