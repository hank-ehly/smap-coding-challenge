# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_http_methods

from consumption.models import User, Consumption


class SummaryView(generic.ListView):
    model = User
    template_name = 'consumption/summary.html'


class DetailView(generic.DetailView):
    model = User
    template_name = 'consumption/detail.html'


@require_http_methods(['GET'])
def consumptions(request, *args, **kwargs):
    user_id = request.GET.get('user_id')

    if user_id is None:
        consumptions = Consumption.objects
    else:
        consumptions = Consumption.objects.filter(user_id=user_id)

    qs = consumptions.annotate(time=TruncDay('datetime')).values('time').annotate(consumption=Sum('consumption'))
    return JsonResponse({'data': list(qs)})
