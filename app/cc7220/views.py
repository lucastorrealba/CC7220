from django.shortcuts import render,redirect
from cc7220.forms import SearchByNameForm
from django import views
from django.http import JsonResponse
from cc7220.extra.queries import Queries
import json


# Create your views here.
class Index(views.View):
    def get(self, request):
        form = SearchByNameForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = SearchByNameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            query = """
            SELECT DISTINCT ?name ?countryname ?year
             WHERE {
              ?scientist wdt:P106 wd:Q901 ;
                         wdt:P569 ?year;
                         wdt:P27 ?country ;
                         rdfs:label ?name .
              ?country rdfs:label ?countryname .
              FILTER (lang(?name)="en") .
              FILTER (lang(?countryname)="en") .
              }
            """
            #res = return_sparql_query_results(query)
            #return redirect('index', {'query': json2html.convert(json=res)})


# Cantidad de cientificos por pais
def q1(request):
    labels = []
    data = []
    query = Queries.get_ccbc(limit=10)
    for d in query:
        if type(d) is dict:
            labels.append(d['country']['value'])
            data.append(d['number']['value'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


class CCBC (views.View):
    def get(self, request):
        return render(request, "ccbc.html")


# Mayores causas de muerte de los científicos
def q2(request):
    labels = []
    data = []
    query = Queries.get_mcmc(limit=10)
    for d in query:
        if type(d) is dict:
            labels.append(d['causes']['value'])
            data.append(d['humans']['value'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


class MCMC (views.View):
    def get (self, request):
        return render(request, "mcmc.html")


# Lista de ocupaciones científicas
def q3():
    table = []
    query = Queries.get_loc()
    for d in query:
        if type(d) is dict:
            table.append(d['scientific_occupations']['value'])
    return table


class LOC(views.View):
    def get(self, request):
        table = q3()
        return render(request, "loc.html", {"table": table})


# cantidad de cientificos por campo de estudio
def q4(request):
    labels = []
    data = []
    query = Queries.get_ccce(limit=10)
    for d in query:
        if type(d) is dict:
            labels.append(d['subjectname']['value'])
            data.append(d['count']['value'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


class CCCE(views.View):
    def get(self, request):
        return render(request, "ccce.html")


# paises donde NACIERON los cientificos
def q5(request):
    labels = []
    data = []
    query = Queries.get_pdnc(limit=15)
    for d in query:
        if type(d) is dict:
            labels.append(d['subjectname']['value'])
            data.append(d['count']['value'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


class PDNC(views.View):
    def get(self, request):
        return render(request, "pdnc.html")


# científicos en guerras
def q6():
    table = []
    query = Queries.get_ceg()
    for d in query:
        table.append(d)
    return table


class CEG(views.View):
    def get(self, request):
        table = q6()
        return render(request, "ceg.html", {"table": table})
