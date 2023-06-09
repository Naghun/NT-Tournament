from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
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

class Bonus_view(TemplateView):
    template_name='game/bonus.html'

class Draft_view(ListView):
    model=Card
    template_name='game/draft.html'
    context_object_name='draft_list'

    def get(self, request):
        cards=self.get_random_cards()
        self.store_cards_in_sessions(request, cards)
        context= {'cards': cards}
        return render(request, 'game/draft.html')
    
    def post(self, request):
        cards=self.get_random_cards()
        self.store_cards_in_sessions(request, cards)
        context={'cards': cards}
        return render(request, 'game/draft.html', context)


    def get_random_cards(self):
        all_cards=list(Card.objects.all())
        random_cards=random.sample(all_cards, 32)
        return random_cards
    
    def store_cards_in_sessions(self, request, cards):
        card_ids= [card.id for card in cards]
        request.session['card_ids']=card_ids
        request.session.modified= True


class Tournament_view(TemplateView):
    template_name='game/tournament.html'