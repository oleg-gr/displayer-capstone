from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import authenticate

from ui.models import *

from django.http import HttpResponse, HttpResponseBadRequest

import json

from datetime import datetime




# Decorators for login checks

@login_required
def index(request):
    # redirect based on whether a user is a display or not
    current_user = request.user
    if is_display_check(current_user):
        return redirect('ui.views.display')
    else:
        if Schedule.objects.filter(user = request.user):
            return redirect('ui.views.manage')
        else:
            return redirect('ui.views.tasks')

def is_not_display_check(user):

    return not is_display_check(user)

def is_display_check(user):

    # an annoying way to determine whether a user is a Display
    is_display = False
    try:
        is_display = (user.display is not None)
    except Display.DoesNotExist:
        pass

    return is_display





# Display logic

@login_required
@user_passes_test(is_display_check, redirect_field_name='/manage')
def display(request):
    context = {}
    return render(request, 'display.html', context)


# Display API endpoints
@login_required
@user_passes_test(is_display_check, redirect_field_name='/manage')
def display_heartbeat(request):
    # updates last_active variable on display
    display = Display.objects.get(user=request.user)
    display.last_active = datetime.now()
    display.save()
    return HttpResponse('')


@login_required
@user_passes_test(is_display_check, redirect_field_name='/manage')
def display_data(request):
    display = Display.get_data_for_display(request.user)
    data = json.dumps(display)
    return HttpResponse(data, content_type='application/json')




# User logic

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def manage(request):
    schedules = Schedule.get_list_of_schedules(request.user)
    context = { 'schedules' : schedules }
    return render(request, 'manage.html', context)

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def tasks(request):
    schedules = Schedule.get_list_of_schedules(request.user)
    context = { 'schedules' : schedules }
    return render(request, 'tasks.html', context)

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def displays(request):
    # Lists basic info about displays
    list_of_displays = Display.get_basic_display_info()
    context = { 'displays' : list_of_displays }
    return render(request, 'displays.html', context)

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def custom_task(request):
    context = {}
    return render(request, 'custom_task.html', context)

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def schedule(request):
    # try:
    if request.method == 'POST':
        data = json.loads(request.POST['json_data'])
        print data
        files = data["files"]
        description = data["description"]
        dates = data["dates"]
        options = data["options"]
        task_type = data["task_type"]

        task = Task(user_id=request.user.id,
            description=description,
            type=Capability.objects.get(id=task_type),
            public=False)

        task.save()

        for file in files:
            media = Media(media="uploads/" + file['uuid'] + "/" + file['name'],
                task=task,
                uuid=file['uuid'])
            media.save()

        displays = []
        screens = options['screens']
        if screens == 'all':
            displays = Display.objects.all()
        elif isinstance(screens, list):
            for screen in screens:
                displays.append(Display.objects.get(id=int(screen)))
        else:
            displays = Display.objects.filter(location=Location.objects.get(id=int(screens)))
            if not displays:
                return HttpResponseBadRequest('No displays at selected location')

        print dates['start']
        print datetime.strptime(dates['start'], "%d/%m/%Y")

        schedule = Schedule(user_id=request.user.id,
            task=task,
            start=datetime.strptime(dates['start'], "%d/%m/%Y"),
            end=datetime.strptime(dates['end'], "%d/%m/%Y"),
            options=options)

        schedule.save()

        for display in displays:
            schedule.displays.add(display)

    else:
        return HttpResponseBadRequest('Should be a POST request')
    # except:
    #     return HttpResponseBadRequest('Something went wrong, please contact administrator')

    return HttpResponse(200, "OK")

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def schedule_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return render(request, 'schedule_task.html',
            { 'error' : "Requested task does not exist." })
    if not task.public and task.user != request.user:
        return render(request, 'schedule_task.html',
            { 'error' : "You cannot edit requested task." })
    if task.public:
        start = datetime.now().strftime("%d/%m/%Y")
        end = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    else:
        start = task.start.strftime("%d/%m/%Y")
        end = task.end.strftime("%d/%m/%Y")
    places = Location.objects.all()
    screens = Display.objects.all()
    context = { 'task_type' : task.type.id,
        'is_public' : task.public,
        'description' : task.description,
        'start' : start,
        'end' : end,
        'places' : places,
        'screens' : screens
        }
    return render(request, 'schedule_task.html', context)


# User API endpoints

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def displays_login_info(request):
    # Lists whether displays are logged in or not
    displays_login_information = Display.get_login_info()
    data = json.dumps(displays_login_information)
    return HttpResponse(data, content_type='application/json')

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def schedules_active_info(request):
    # Lists whether displays are logged in or not
    schedules_active_info = Schedule.get_schedules_active_info(request.user)
    print schedules_active_info
    data = json.dumps(schedules_active_info)
    return HttpResponse(data, content_type='application/json')
