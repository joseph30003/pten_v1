from django.http import HttpResponse
from django.template.loader import get_template
import datetime
from django.shortcuts import render
import json,requests

def homepage(request):
    return HttpResponse("This is clinical trial matching website")

def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('time.html')
    html = t.render({'current_date':now,'name_list':["abhishek","talluri"]})
    return HttpResponse(html)
	
def trial_list(request):
	data = {
    "query": {
        "query_string": { "query": "cancer" }
			}
	}
	records = requests.post('http://127.0.0.1:9200/testindex/trials/_search', data=json.dumps(data))
	records = records.json()["hits"]["hits"]
	ls = []
	for i in records:
		rec = {}
		rec['title'] = i['_source']['title']
		rec['purpose'] = i['_source']['purpose']
		ls.append(rec)
	records = ls
	return render(request,'trialmatch/trial_list.html',{'records':records})