from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
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
        if 'delete_cards' in request.POST:
            if 'card_ids' in request.session:
                del request.session['card_ids']
                request.session.modified = True
            cards = []

        else:
            card_ids = request.session.get('card_ids')
            if card_ids:
                cards = Card.objects.filter(id__in=card_ids)
            else:
                cards = []

        context = {'cards': cards}
        return render(request, self.template_name, context)
    
    def post(self, request):
        if 'delete_cards' in request.POST:
            if 'card_ids' in request.session:
                del request.session['card_ids']
                request.session.modified = True
            cards = []
        else:
            card_ids = request.session.get('card_ids')
            if card_ids:
                cards = Card.objects.filter(id__in=card_ids)
            else:
                cards, card_ids = self.get_random_cards()
                request.session['card_ids'] = card_ids
                request.session.modified = True

        context = {'cards': cards}
        return render(request, self.template_name, context)

    def get_random_cards(self):
        human_cards=list(Card.objects.filter(id__range=(1,20)))
        drawn_human_cards=list(random.sample(human_cards, 8))

        fantasy_cards=list(Card.objects.filter(id__range=(21,40)))
        drawn_fantasy_cards=list(random.sample(fantasy_cards, 8))

        creature_cards=list(Card.objects.filter(id__range=(41,60)))
        drawn_creature_cards=list(random.sample(creature_cards, 8))

        alien_cards=list(Card.objects.filter(id__range=(61,80)))
        drawn_alien_cards=list(random.sample(alien_cards, 8))

        random_cards=drawn_human_cards+drawn_fantasy_cards+drawn_creature_cards+drawn_alien_cards
        random.shuffle(random_cards)
        card_ids = [card.id for card in random_cards]
        return random_cards, card_ids

class Tournament_view(TemplateView):
    template_name='game/tournament.html'

class PairsView(ListView):
    template_name='game/pairs.html'
    model=Card

    def get_pairs(self):
        cards_id=self.request.session.get('card_ids')
        return cards_id
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_cards']=self.get_pairs()
        return context