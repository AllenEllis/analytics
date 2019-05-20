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
    response = "You're looking at the report for report %s."
    response += category
    return HttpResponse(response % name)


