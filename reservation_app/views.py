from django.shortcuts import render, HttpResponse, redirect
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
        room_has_projector = request.POST.get('room-projector') == 'on'
        if room_name == '':
            return TemplateResponse(request, 'new-room-form-name-error.html')
        elif room_capacity == '' or int(room_capacity) < 0:
            return TemplateResponse(request, 'new-room-form-capacity-error.html')
        elif ConfRoom.objects.filter(name=room_name).first():
            return TemplateResponse(request, 'new-room-form-duplicate-name.html')
        # dopisz: if'a czy sala już istnieje w bazie
        else:
            ConfRoom.objects.create(name=room_name, capacity=room_capacity, projector_availability=room_has_projector)
            return redirect('/room/list')


def room_list(request):
    room_list = []
    for conf_room in ConfRoom.objects.all():
        room = {'id': conf_room.id, 'name': conf_room.name, 'capacity': conf_room.capacity, 'projector': conf_room.projector_availability}
        room_list.append(room)
    ctx = {
        'room_list': room_list
    }
    return TemplateResponse(request, 'room-list.html', ctx)


def room_details(request, room_id):
    current_room = ConfRoom.objects.filter(pk=room_id)
    room = {}
    for room_data in current_room:
        room = {'id': room_data.id,
                'name': room_data.name,
                'capacity': room_data.capacity,
                'projector': room_data.projector_availability}
    ctx = {
        'room_details': room
    }
    return TemplateResponse(request, 'room-details.html', ctx)


def room_delete(request, room_id):
    if request.method == 'GET':
        delete_action = ConfRoom.objects.filter(pk=room_id).delete()
        delete_number = delete_action[1]['reservation_app.ConfRoom']
        message = f'Usunięto {delete_number} salę'
        ctx_message = {
            'message': message
        }
    return redirect('/room/list', ctx_message)


def room_modify(request, room_id):
    if request.method == 'GET':
        search_action = ConfRoom.objects.filter(pk=room_id)
        room = {}
        for room_details in search_action:
            room = {
                'id': room_details.id,
                'name': room_details.name,
                'capacity': room_details.capacity,
                'projector': room_details.projector_availability
            }
        ctx = {
            'room': room
        }
        return TemplateResponse(request, 'modify-room-form.html', ctx)