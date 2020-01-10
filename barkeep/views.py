from django.shortcuts import render

from barkeep.models import Pump


def index(request):
    return render(request, 'barkeep/index.html', {
        'pumps': Pump.objects.all
    })
