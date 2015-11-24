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
	
	return render(request,'trialmatch/trial_list.html')
	
def trialpage(request):
	value = request.GET['rec']
	path = 'http://127.0.0.1:9200/clinicaltrials/mappedTrials_v2/' + value
	record = requests.get(path)
	record = record.json()
	rec = {}
	rec["source"] = {}
	rec["source"]["IC"] = {}
	rec["source"]["EC"] = {}
	for field in record:
		if field == "_source":
			rec["source"] = record[field]
			if "maximumAge" in record[field]:
				rec["source"]["maximumAge"] = int(record[field]["maximumAge"])/525600
			if "minimumAge" in record[field]:
				rec["source"]["minimumAge"] = int(record[field]["minimumAge"])/525600
			if "Inclusion Criteria" in record[field]:
				rec["source"]["IC"] = record[field]["Inclusion Criteria"]
			if "Exclusion Criteria" in record[field]:
				rec["source"]["EC"] = record[field]["Exclusion Criteria"]
		elif field == "_id":
			rec["id"] = record[field]
		else:
			rec[field] = record[field]	
	return render(request,'trialmatch/trialpage.html',{'rec':rec})

def search(request):
	disease = request.POST['diseaseType']
	gene = request.POST['geneType']
	age = request.POST['age']
	gender = request.POST['gender']
	aas = request.POST['aas']
	stage = request.POST['stage']
	
	
	body = {}
	body["query"] = {}
	body["query"]["bool"] = {}
	body["query"]["bool"]["must"] = []
	body["query"]["bool"]["should"] = []
	
	body["highlight"] = {}
	body["highlight"]["fields"] = {}
	body["highlight"]["fields"]["Purpose"] = {"number_of_fragments":0}
	body["highlight"]["fields"]["official_title"]={"number_of_fragments":0}
	body["highlight"]["pre_tags"] = ["<mark>"]
	body["highlight"]["post_tags"] = ["</mark>"]
			
	if disease:
		body["query"]["bool"]["must"].append({
                        "multi_match":
                        {
                            "query": disease,
                            "boost":3,
                            "fields": ["Purpose","description","Inclusion Criteria","official_title","brief_title","Conditions",
                                       "Purpose.whitespace","description.whitespace","Inclusion Criteria.whitespace","official_title.whitespace","brief_title.whitespace","Conditions.whitespace"]}})
		body["query"]["bool"]["should"].append({
          "multi_match": {
                  "query" : disease,
                  "boost" : 0.1,
                  "fields" : ["Exclusion Criteria","Exclusion Criteria.whitespace","Exclusion Criteria.normal"]
                }

        	})
	if gene:
		body["query"]["bool"]["must"].append({
                        "multi_match":
                        {
                            "query": gene,
                            "boost" :3,
                            "fields": ["Purpose","description","Inclusion Criteria","official_title","brief_title","Conditions",
                                       "Purpose.whitespace","description.whitespace","Inclusion Criteria.whitespace","official_title.whitespace","brief_title.whitespace","Conditions.whitespace"]}})
		body["query"]["bool"]["should"].append({
          "multi_match": {
                  "query" : gene,
                  "boost" : 0.1,
                  "fields" : ["Exclusion Criteria","Exclusion Criteria.whitespace","Exclusion Criteria.normal"]
                }})
	if age:
		body["query"]["bool"]["must"].append({
                        "range":{
                            "maximumAge":{"gte": int(age) * 365 * 24 * 60}}})
		body["query"]["bool"]["must"].append({
                        "range":{
                            "minimumAge":{"lte": int(age) * 365 * 24 * 60}}})
	body["query"]["bool"]["must"].append({"bool": {}})
	body["query"]["bool"]["must"][-1]["bool"]["should"] = []
	
	if gender:
		body["query"]["bool"]["must"][-1]["bool"]["should"].append({
                                "match": {
                                    "gender": gender
                                }})
		body["query"]["bool"]["must"][-1]["bool"]["should"].append({
                                "match": {
                                    "gender": "Both"
                                }})
	if aas:
		body["query"]["bool"]["must"].append({
          "multi_match": {
            "query": aas,
            "boost" :3,
            "fields": ["Purpose","description","Inclusion Criteria","official_title","brief_title","Conditions",
                       "Purpose.whitespace","description.whitespace","Inclusion Criteria.whitespace","official_title.whitespace","brief_title.whitespace","Conditions.whitespace"]}})

		body["query"]["bool"]["should"].append({
          "multi_match": {
                  "query" : aas,
                  "boost" : 0.1,
                  "fields" : ["Exclusion Criteria","Exclusion Criteria.whitespace","Exclusion Criteria.normal"]
                }

        	})
	records = requests.post('http://127.0.0.1:9200/clinicaltrials/mappedTrials_v2/_search', data=json.dumps(body))
	records = records.json()["hits"]["hits"]
	ls = []

	for i in records:
		rec = {}
		for field in i:
			if field == "_source":
				rec["source"] = i[field]
			elif field == "_id":
				rec["id"] = i[field]
			else:
				rec[field] = i[field]
			
		ls.append(rec)
	records = ls    	#t = loader.get_template('template/trial_list.html',{'records':records})
   	#c = Context({ 'query': query,})
	return render(request,'trialmatch/searchResults.html',{'records': ls})
	
def testsearch(request):
	disease = request.POST['diseaseType']
	gene = request.POST['geneType']
	age = request.POST['age']
	gender = request.POST['gender']
	aas = request.POST['aas']
	stage = request.POST['stage']
	
	
	body = {}
	body["query"] = {}
	body["query"]["bool"] = {}
	body["query"]["bool"]["must"] = []
	body["query"]["bool"]["should"] = []
	
	body["highlight"] = {}
	body["highlight"]["pre_tags"] = ["<mark>"]
	body["highlight"]["post_tags"] = ["</mark>"]
	body["highlight"]["fields"] = {}
	body["highlight"]["fields"]["title"] = {}
	body["highlight"]["fields"]["purpose"] = {}
	
	if disease:
		body["query"]["bool"]["must"].append({
                        "multi_match":
                        {
                            "query": disease,
                            "boost":3,
                            "fields": ["title","purpose"]}})
		
	if gene:
		body["query"]["bool"]["must"].append({
                        "multi_match":
                        {
                            "query": gene,
                            "boost" :3,
                            "fields": ["title","purpose"]}})
	if aas:
		body["query"]["bool"]["must"].append({
          "multi_match": {
            "query": aas,
            "boost" :3,
            "fields": ["title","purpose"]}})

		       
	records = requests.post('http://127.0.0.1:9200/testindex/trials/_search', data=json.dumps(body))
	records = records.json()["hits"]["hits"]
	ls = []
	for i in records:
		rec = {}
		rec['Title'] = i['_source']['title']
		rec['Purpose'] = i['highlight']['purpose']
		ls.append(rec)
	records = ls    	#t = loader.get_template('template/trial_list.html',{'records':records})
   	#c = Context({ 'query': query,})
	return render(request,'trialmatch/searchResults.html',{'records':records})