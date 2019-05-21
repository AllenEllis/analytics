from django.shortcuts import render
from .models import Report
from .models import Category
from django.http import HttpResponse


def index(request):
    return render(request, 'reports/index.html')


def nav(request):
    reports = Report.objects.filter()
    categories = Category.objects.filter()
    context = {'categories': categories, 'reports': reports}
    return render(request, 'reports/nav.html', context)


def report(request, category, name):
    #report = Report.objects.get(id__exact=)
    #context = { 'report': report }
    #return render(request, 'reports/report.html', context)
    return HttpResponse("This is where the report would go")


