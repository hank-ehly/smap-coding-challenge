# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from consumption.models import User


class SummaryView(generic.ListView):
    model = User
    template_name = 'consumption/summary.html'

    def get_queryset(self):
        return User.objects.all()


def detail(request):
    context = {
    }
    return render(request, 'consumption/detail.html', context)
