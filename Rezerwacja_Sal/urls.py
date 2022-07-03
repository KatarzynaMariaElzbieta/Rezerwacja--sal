"""Rezerwacja_Sal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hall_reservation.views import main, NewRoom, ModifyRoom, BookRoom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('room/new', NewRoom.as_view(), name='new_room'),
    path('room/modify/<int:id>', ModifyRoom.as_view(), name='new_room'),
    # path('room/delete/<int:id>', Delete.as_view(), name='delete_room'),
    # path('room/<int:id>', RoomInfo.as_view(), name='info_room'),
    path('reservation/<int:id>', BookRoom.as_view(), name='book_room'),

]
