from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import ConfRoom, RoomReservation
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
# Create your views here.

TODAY = str(date.today())

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
        elif room_capacity == '' or int(room_capacity) <= 0:
            ctx = {
                'error_message': 'Podaj pojemność (musi być większe niż zero).'
            }
            return TemplateResponse(request, 'new-room-form.html', ctx)
            # return HttpResponse('Podaj pojemność (musi być większe niż zero).'
            # return TemplateResponse(request, 'new-room-form-capacity-error.html')
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
    current_reservations = RoomReservation.objects.filter(conf_room=room_id)
    reservations = {}
    for reservation in current_reservations:
        reservations = {
            'date': reservation.date,
            'comment': reservation.comment
        }
    ctx['reservations'] = reservations
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


@csrf_exempt
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
    if request.method == 'POST':
        new_room_name = request.POST.get('room-name')
        new_room_capacity = request.POST.get('room-capacity')
        new_room_projector = request.POST.get('room-projector') == 'on'
        if int(new_room_capacity) > 0 and new_room_name:
            for room in ConfRoom.objects.filter(pk=room_id):
                room.name = new_room_name
                room.capacity = new_room_capacity
                room.projector_availability = new_room_projector
                room.save()
            return redirect('/room/list')
        else:
            return TemplateResponse(request, 'modify-room-form-capacity-error.html')


@csrf_exempt
def room_reserve(request, room_id):
    # Fetch conf room data
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
    # Display form
    if request.method == 'GET':
        return TemplateResponse(request, 'room-reservation.html', ctx)
    elif request.method == "POST":
        my_room = get_object_or_404(ConfRoom, pk=room_id)
        reserve_date = request.POST.get('reservation-date')

        # Error handling for old date
        if reserve_date < TODAY:
            ctx['error_message'] = 'Wybrana data jest z przeszłości'
            return TemplateResponse(request, 'room-reservation.html', ctx)

        # Error handling for already reserved conf room
        if RoomReservation.objects.filter(conf_room=room_id, date=reserve_date):
            ctx['error_message'] = 'Sala jest zajęta w tym terminie.'
            return TemplateResponse(request, 'room-reservation.html', ctx)

        # Adding reservation to database
        reserve_comment = request.POST.get('reservation-comment')
        RoomReservation.objects.create(conf_room=my_room, date=reserve_date, comment=reserve_comment)
        return redirect('/room/list')
