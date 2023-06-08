from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Card
import random
from django.http.response import JsonResponse

# Create your views here.
class Start_view(TemplateView):
    template_name='game/start.html'

class List_view(ListView):
    model=Card
    template_name='game/list.html'
    context_object_name='data_of_cards'
    
class Cards_view(ListView):
    model=Card
    template_name='game/cards.html'
    context_object_name='pictures_of_cards'

    def get_random_cards(self):
        random_numbers=random.sample(range(1,81),32)
        random_cards=Card.objects.filter(id__in=random_numbers)
        return random_cards

    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['random_cards']=self.get_random_cards()
        return context


class Bonus_view(TemplateView):
    template_name='game/bonus.html'

class Draft_view(ListView):
    model=Card
    template_name='game/draft.html'
    context_object_name='draft_list'

    def novi_brojevi(self, request):
        random_numbers = random.sample(range(1, 81), 32)
        request.session['random_numbers'] = random_numbers

    def post(self, request, *args, **kwargs):
        if 'novi_brojevi' in request.POST:
            self.novi_brojevi(request)

        return super().get(request, *args, **kwargs)
    

class Tournament_view(TemplateView):
    template_name='game/tournament.html'