import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View
# from importlib_resources._common import _

from hall_reservation.forms import BookForm
from hall_reservation.models import Hall, Reservation


# Create your views here.

def main(request):
    """Widok strony głównej"""
    all_hall = Hall.objects.all()
    print(datetime.date.today())
    reservations = Reservation.objects.filter(date=datetime.date.today())
    print(reservations)
    reserved_today = [book.hall_id for book in reservations]
    print('reserved_today')
    print(reserved_today)
    reservations = Reservation.objects.all()
    # for i in reservations:
    #     print('rp')
    #     print(i.date)
    return render(request, 'main_page.html', {'hall_list': all_hall, 'reservations': reserved_today})


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


class BookRoom(View):
    """Klasa dodająca rezerwująca sale."""

    def get(self, request, id):
        """Formularz rezerwacji sali"""
        room = Hall.objects.get(id=id)
        form = BookForm(initial={'hall_id': room.id})
        # form.initial({'hall_id': room.id})
        return render(request, 'new-book-form.html', {'room': room, 'form': form})

    def post(self, request, id):
        """Funkcja odczytuje z formularza i zapisuje dane nowej rezerwacji sali do bazy"""
        form = BookForm(request.POST)
        if form.is_valid():
            r = Reservation.objects.create(
                date=request.POST.get('date'),
                hall_id=id,
                comment=request.POST.get('comment'),
            )
            return render(request, 'new-book-form.html', {'added': 'Yes', 'reservation': r})
        else:
            return render(request, 'new-book-form.html', {'added': 'No'})
