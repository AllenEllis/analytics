from django.shortcuts import render
from .models import Report
from .models import Category
from . import reports
from django.http import HttpResponse


def index(request):
    return render(request, 'reports/index.html')


def nav(request):
    reports = Report.objects.filter()
    categories = Category.objects.filter()
    context = {'categories': categories, 'reports': reports}
    return render(request, 'reports/nav.html', context)


def report(request, category, name, id):
    report = Report.objects.get(id__exact=id)
    html = report.render()
    context = { 'report': report, 'html': html }
    #return render(request, 'reports/report.html',x context)

    #context = {'reports': reports}

    return render(request, 'reports/report.html', context)
    #return HttpResponse(report)


