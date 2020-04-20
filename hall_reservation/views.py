from django.shortcuts import render
from django.views import View

from hall_reservation.models import Hall


# Create your views here.

def glowna(request):
    """Widok strony głównej"""
    return render(request, 'index.html', {})


class NewRoom(View):
    """Klasa dodająca nowe sale."""

    def get(self, request):
        """Formularz dodania nowej sali"""
        return render(request, 'new-hall-form.html', {'added': 'yes'})

    def post(self, request):
        """Funkcja odczytuje z formularza i zapisuje dane nowej sali do bazy"""
        try:
            room = Hall.objects.create(
                name=request.POST.get("name"),
                seats=request.POST.get("seats"),
                projector=request.POST.get("projector")
            )
            return render(request, 'new-hall-form.html', {'added': 'Yes'})
        except:
            return render(request, 'new-hall-form.html', {'added': 'No'})


class ModifyRoom(View):
    """Klasa dodająca nowe sale."""

    def get(self, request, id):
        """Formularz edycji sali"""
        print(id)
        room = Hall.objects.get(id=id)
        return render(request, 'modify-hall-form.html', {'room': room})

    def post(self, request, id):
        """Funkcja odczytuje z formularza i zapisuje dane nowej sali do bazy"""
        try:
            room = Hall.objects.get(pk=id)
            room.name = request.POST.get("name")
            room.seats = int(request.POST.get("seats"))
            room.projector = request.POST.get("projector")
            room.save()
            return render(request, 'modify-hall-form.html', {'modify': 'Yes'})

        except:
            return render(request, 'modify-hall-form.html', {'modify': 'No'})
