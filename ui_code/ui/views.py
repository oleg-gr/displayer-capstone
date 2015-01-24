from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate

from ui.models import Display

@login_required
def index(request):
    displays = Display.objects.order_by('id')
    context = {}
    return render(request, 'index.html', context)

