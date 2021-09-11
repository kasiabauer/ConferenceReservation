from django.shortcuts import render, HttpResponse
from .models import ConfRoom
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def new_room(request):
    if request.method == "GET":
        return TemplateResponse(request, 'new-room-form.html')
    if request.method == 'POST':
        room_name = request.POST.get('room-name')
        room_capacity = request.POST.get('room-capacity')
        if room_name == '':
            return TemplateResponse(request, 'new-room-form-name-error.html')
        elif room_capacity == '' or int(room_capacity) < 0:
            return TemplateResponse(request, 'new-room-form-capacity-error.html')
        # dopisz: if'a czy stala już istnieje w bazie
        else:
            return HttpResponse(request, 'new-room-form.html')
