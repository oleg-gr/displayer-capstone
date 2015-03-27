# TO-DO:
# - Figure out why index.html doesn't redirect



from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import authenticate

from ui.models import Display, User, Schedule

from django.http import HttpResponse

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
        return redirect('ui.views.manage')

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
    display = Display.get_for_display(request.user)
    context = {'display':display}
    return render(request, 'display.html', context)


# Display API endpoints
@login_required
@user_passes_test(is_display_check, redirect_field_name='/heartbeat')
def display_heartbeat(request):
    # updates last_active variable on display
    display = Display.objects.get(user=request.user)
    display.last_active = datetime.now()
    display.save()
    return HttpResponse('')




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
    context = {}
    return render(request, 'tasks.html', context)

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def displays(request):
    # Lists basic info about displays
    list_of_displays = Display.get_basic_display_info()
    context = { 'list_of_displays' : list_of_displays }
    return render(request, 'displays.html', context)

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def custom_task(request):
    context = {}
    return render(request, 'custom_task.html', context)


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
    data = json.dumps(schedules_active_info)
    return HttpResponse(data, content_type='application/json')
