from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import default_storage
from django.core import serializers
import json

from . import forms as f
from . import file_analyzer
from . import benford
from .models import DataSets
from .models import BenfordDistributions

id = 0
file_analize = None
file_name = None

def history(request: HttpRequest) -> HttpResponse:
    dv = DataSets.objects.all()    
    return render(request, 'history.html', {'user_sets': dv})


def upload(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = f.UploadForm()
    elif request.method == "POST":
        
        form = f.UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['the_file']
            txt = (f"filename: {file.name}  filesize: {file.size}")
            name = form.cleaned_data['user_name']
            dataset = form.cleaned_data['dataset_name']
            saved_data = form.save()
            global id, file_name, file_analize
            
            id = saved_data.id
            file_name = default_storage.save(file.name, file)            
            file_analize = file_analyzer.FileAnalyzer(default_storage.open(file_name))

            headers, datatype = file_analize.readHeaders()
            print (f'heads: {headers}')
            if headers == 'Error occured':
                default_storage.delete(file_name)
                return render(request, 'upload.html', {'form': form, "no_columns": True, 'no_desired_column': True})
            
            hasDesiredColumn = file_analize.checkRequiredColumn(headers)
            if hasDesiredColumn:
                col = '7_2009'
                dict_data = processBenford(file_name, file_analize, col, id)
                if type(dict_data) == str:
                    return render(request, 'upload.html', {'form': form, "result": False, 'no_desired_column': True})

                temp = []
                for i in '123456789':
                    temp.append({'num': i, 'your': round(dict_data['first_number'][i]*100,2), 'ben': round(dict_data['Benford'][i]*100, 2)})
                print(temp)
                return render(request, 'tableGraph.html', context = {"result": True, 'dict_data': dict_data, 'temp':temp })
            else:
                columns = file_analize.findNumericColumns()
                default_storage.delete(file_name)
                return render(request, 'upload.html', {'form': form, "columns": columns, 'no_desired_column': True,  "no_columns": False,})
            
    else:
        raise NotImplementedError
    
    return render(request, 'upload.html', {'form':form})


def postColumn(request: HttpRequest) -> HttpResponse:
    if request.is_ajax and request.method == 'POST':
        print(request.POST)
        col =  request.POST.get('column', None)
        dict_data = processBenford(file_name, file_analize, col, id)
        if type(dict_data) == str:
            dict = {'low': True}
            return HttpResponse(json.dumps(dict), content_type='application/json')

        temp = []
        for i in '123456789':
            temp.append({'num': i, 'your': round(dict_data['first_number'][i]*100,2), 'ben': round(dict_data['Benford'][i]*100, 2)})
        
        #print(temp)
        return render(request, 'tableOnly.html', context = {"result": True, 'dict_data': dict_data, 'temp':temp })
        

def processBenford(file_name, file_analize, col, id):
    df = file_analize.getRequiresDataSet(col)
    ben = benford.BenfordDataset(df,id,col)
    dict_data = ben.get_benford_distribution()
    if type(dict_data) == str:
        return dict_data
    is_saved = ben.save_results()
    default_storage.delete(file_name)
    return dict_data

def getSavedSet(request: HttpRequest) -> HttpResponse:
    if request.is_ajax and request.method == 'POST':
        set_id =  request.POST.get('set_id', None)
        dv = DataSets.objects.get(id=int(set_id))
        benfords = BenfordDistributions.objects.filter(dataset__id= int(set_id))
        ben = serializers.serialize('json', benfords, ensure_ascii=False)
        bens = json.loads(ben)
        temp = []
        for b in bens:
            print(type(b))
            print(b)
            print(b['fields']['occurence'])
            temp.append({'num': b['fields']['number'], 'your': round(b['fields']['occurence']*100,2), 'ben': round(b['fields']['bensfords']*100,2)})

        return render(request, 'tableOnly.html', context = {"result": True, 'dict_data': temp, 'temp':temp })