from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from iw.models import Facility
import json


# Create your views here.
def homepage(request):
    context = {}
    context['plans'] = Facility.objects.filter(category="floorplan")
    return render(request, 'homepage.html', context=context)


def heating(request):
    context = {}
    context['plans'] = Facility.objects.filter(category="floorplan")
    context['legends'] = Facility.objects.filter(category="heating")
    return render(request, 'heating.html', context=context)


def ventilation(request):
    context = {}
    context['plans'] = Facility.objects.filter(category="floorplan")
    context['legends'] = Facility.objects.filter(category="ventilation")
    return render(request, 'ventilation.html', context=context)


def ac(request):
    context = {}
    context['plans'] = Facility.objects.filter(category="floorplan")
    context['legends'] = Facility.objects.filter(category="ac")
    return render(request, 'ac.html', context=context)


def lighting(request):
    context = {}
    context['plans'] = Facility.objects.filter(category="floorplan")
    context['legends'] = Facility.objects.filter(category="lighting")
    return render(request, 'lighting.html', context=context)


def getPlanImage(request, id):
    image = get_object_or_404(Facility, id = id)
    if not image.picture:
        raise Http404
    return HttpResponse(image.picture, content_type=image.content_type)