from django.shortcuts import render
from django.views import View

# Create your views here.

def glowna(request):
    return render(request, 'index.html', {})


class NewRoom(View):
    def get(self, request):
        return render(request, 'new-hall-form.html', {})

    def post(self, request):
        pass
