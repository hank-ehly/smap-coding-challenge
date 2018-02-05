# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import http
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.decorators.http import require_http_methods

from consumption.encoders import ConsumptionRollupEncoder
from consumption.models import User, ConsumptionRollup


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
    try:
        user = get_object_or_404(User, pk=kwargs['user_id'])
    except http.Http404, ex:
        return JsonResponse({'message': ex.message}, status=404)

    return JsonResponse(list(user.consumptions()), safe=False)
