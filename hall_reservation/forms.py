from django.forms import ModelForm

from hall_reservation.models import Reservation


class BookForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'comment']
