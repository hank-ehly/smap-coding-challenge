# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.serializers import serialize
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.http import require_http_methods

from consumption.encoders import ConsumptionRollupEncoder
from consumption.models import User, Consumption, ConsumptionRollup


class SummaryView(generic.ListView):
    model = User
    template_name = 'consumption/summary.html'


class DetailView(generic.DetailView):
    model = User
    template_name = 'consumption/detail.html'


@require_http_methods(['GET'])
def consumptions(request):
    serialized_data = serialize('json', ConsumptionRollup.objects.all(), cls=ConsumptionRollupEncoder)
    return JsonResponse(serialized_data, safe=False)


@require_http_methods(['GET'])
def user_consumptions(request, *args, **kwargs):
    user_id = int(kwargs['pk'])

    query_set = Consumption.objects \
        .filter(user_id=user_id) \
        .annotate(date=TruncDay('datetime')) \
        .values('date') \
        .annotate(sum=Sum('consumption')) \
        .annotate(average=Avg('consumption'))

    return JsonResponse(list(query_set), safe=False)
