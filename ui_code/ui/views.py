from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import authenticate

from ui.models import Display, User

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

@login_required
@user_passes_test(is_not_display_check, redirect_field_name='/display')
def manage(request):

    context = {}
    return render(request, 'manage.html', context)

@login_required
@user_passes_test(is_display_check, redirect_field_name='/manage')
def display(request):

    context = {}
    return render(request, 'display.html', context)