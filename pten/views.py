from django.shortcuts import *
from validation.models import Index as ES_Index
from django.contrib.auth.decorators import login_required
from pten.forms import QueryForm,OptionsForm
from pten.ElasticSearch import normal,myargs,dis_hier,dis_hier_aas,normal_t1


def get_args(parameters):
	args = myargs()
	if parameters['disease']:
		args.disease = parameters['disease']
	if parameters['gene']:
		args.gene = parameters['gene']
	if parameters['age']:
		args.age = int(parameters['age'])
	if parameters['gender']:
		args.gender = parameters['gender']
	if parameters['aas']:
		args.aas = parameters['aas']
	if parameters['stage']:
		args.stage = parameters['stage']
	if parameters['grade']:
		args.stage = parameters['grade']
	return args


def ElasticSearch(query,option):
	index_file = option['ElasticSearch']
	if option['Ontology'] :
		res,count = dis_hier(query,index_file.index_name)
		hier = 'dis'
		return res,count,hier
	elif option['aas_on'] :
		res,count = dis_hier_aas (query, index_file.index_name)
		hier = 'aas'
		return res, count,hier
	else:
		if index_file.index_name == 'test_transfer1':

			res,count = normal_t1(query,index_file.index_name)

		else:
			res, count = normal(query, index_file.index_name)

		hier = ''
		return res, count,hier

@login_required ()
def Query_view(request):
	hier = False
	ct_list = []
	profile = {}
	total_num = 0
	if request.method == 'POST':
		Qform=QueryForm(request.POST)
		Oform=OptionsForm(request.POST)
		if Qform.is_valid() and Oform.is_valid():
			query=get_args(Qform.cleaned_data)
			print(query.gender)
			profile={key:Qform.cleaned_data[key] for key in Qform.fields}

		#ct_list,total_num = normal(query,index_file.index_name)
			ct_list, total_num,hier = ElasticSearch(query,Oform.cleaned_data)


	else:
		Qform = QueryForm()
		Oform = OptionsForm()

	return render(request,'trialmatch.html',{'query_form':Qform,'option_form':Oform,'ctlist':ct_list,'total':total_num,'hier':hier,'profile':profile})

def Query_view_2(request):
	hier = False
	ct_list = []
	profile = {}
	total_num = 0
	if request.method == 'POST':
		Qform=QueryForm(request.POST)
		Oform=OptionsForm(request.POST)
		if Qform.is_valid() and Oform.is_valid():
			query=get_args(Qform.cleaned_data)
			print(query.gender)
			profile={key:Qform.cleaned_data[key] for key in Qform.fields}

		#ct_list,total_num = normal(query,index_file.index_name)
			ct_list, total_num,hier = ElasticSearch(query,Oform.cleaned_data)


	else:
		Qform = QueryForm()
		Oform = OptionsForm()

	return render(request,'trialmatch.html',{'query_form':Qform,'option_form':Oform,'ctlist':ct_list,'total':total_num,'hier':hier,'profile':profile})
