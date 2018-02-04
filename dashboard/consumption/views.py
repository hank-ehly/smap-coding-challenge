# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from consumption.models import User, Consumption


class SummaryView(generic.ListView):
    model = User
    template_name = 'consumption/summary.html'


def consumption_summary(request, *args, **kwargs):
    qs = Consumption.objects.annotate(time=TruncDay('datetime')).values('time').annotate(consumption=Sum('consumption'))
    return JsonResponse({'results': list(qs)})


def detail(request):
    context = {
    }
    return render(request, 'consumption/detail.html', context)
