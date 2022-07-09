import calendar
import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render
from django.views import View

from hall_reservation.forms import BookForm
from hall_reservation.models import Hall, Reservation


# Create your views here.

def main(request):
    """Widok strony głównej"""
    all_hall = Hall.objects.all()
    reservations = Reservation.objects.filter(date=datetime.date.today())
    reserved_today = [book.hall_id for book in reservations]
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
            return render(request, 'new-hall-form.html', {'added': 'Yes', 'room': room})
        except ValidationError:
            return render(request, 'new-hall-form.html', {'added': 'No'})


class ModifyRoom(View):
    """Klasa dodająca nowe sale."""

    def get(self, request, id):
        """Formularz edycji sali"""
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
        except ValidationError:
            return render(request, 'modify-hall-form.html', {'modify': 'No'})


class BookRoom(View):
    """Klasa dodająca rezerwująca sale."""

    def get(self, request, id, rdate=datetime.date.today().strftime('%Y-%m-%d')):
        """Formularz rezerwacji sali"""
        room = Hall.objects.get(id=id)
        form = BookForm(initial={'hall_id': room.id, 'date': rdate})
        return render(request, 'new-book-form.html', {'room': room, 'form': form})

    def post(self, request, id, rdate):
        """Funkcja odczytuje z formularza i zapisuje dane nowej rezerwacji sali do bazy"""
        try:
            form = BookForm(request.POST)
            if form.is_valid():
                r = Reservation.objects.create(
                    date=request.POST.get('date'),
                    hall_id=id,
                    comment=request.POST.get('comment'),
                )
                return render(request, 'new-book-form.html', {'added': 'Yes', 'reservation': r})
        except IntegrityError:
            return render(request, 'new-book-form.html', {'added': 'occupied'})
        return render(request, 'new-book-form.html', {'added': 'No'})


def drop_hall(request, id):
    """Widok strony głównej"""
    room = Hall.objects.get(id=id)
    room.delete()
    return render(request, 'main_page.html', {'added': 'Yes'})


def room_info(request, id):
    room = Hall.objects.get(id=id)
    month = [week for week in
             calendar.Calendar().monthdatescalendar(datetime.date.today().year, datetime.date.today().month)]
    # reservations = Reservation.objects.filter(hall_id=id).filter(datr_gte=datetime.date.today())
    # print(reservations)
    reservations = room.reservation_set.all()
    reserved_list = [book_date.date.date() for book_date in reservations]
    return render(request, 'hall_details.html', {'hall': room, 'month': month, "reserved_list": reserved_list})
