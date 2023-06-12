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

"""  ################################################################  """

class Bonus_view(ListView):
    model=Card
    template_name='game/bonus.html'

    def get(self, request):
        if 'delete_bonuses' in request.POST:
            if 'bonus_numbers' in request.session:
                del request.session['bonus_numbers']
                request.session.modified=True
            numbers=[]
        else:
            numbers=request.session.get('bonus_numbers')
        bonuses, fighters=self.define_bonuses(request)
        context= {'numbers':numbers, 'bonuses':bonuses, 'fighters':fighters}
        return render(request, self.template_name, context)
    
    def post(self, request):
        if 'delete_bonuses' in request.POST:
            if 'bonus_numbers' in request.session:
                del request.session['bonus_numbers']
                request.session.modified=True
            numbers=[]

        context={'numbers':numbers}
        return render(request, self.template_name, context)
    
    def define_bonuses(self, request):
        flaster=12
        zavoj=18
        napitak_zeleni=24
        boks=-12
        boks_crveni=-18
        napitak_zelenocrni=-24

        mac=6
        dupli_mac=10
        napitak_crveni=14
        zvijezde=-6
        zvijezde_crvene=-10
        napitak_crvenocrni=-14

        stit=4
        oklop=6
        napitak_plavi=8
        knock=-4
        knock_crveni=-6
        napitak_plavo_crni=-8

        numbers=self.get_random_numbers(request)
        bonuses=[]
        card_ids=request.session.get('card_ids')
        drawn_cards=Card.objects.filter(id__in=card_ids)
        fighters={f'fighter{num+1}': [card.id, card.name, card.overall, card.health, card.attack, card.deffence] for num, card in enumerate(drawn_cards)}
        for index, number in enumerate(numbers):
            card_id=index+1
            if number>=1 and number<=200:
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got nothing")
            elif number>200 and number<251:
                fighters[f'fighter{card_id}'][3]+=flaster
                fighters[f'fighter{card_id}'][2]+=flaster
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +12 health")
            elif number>250 and number<301:
                fighters[f'fighter{card_id}'][3]+=zavoj
                fighters[f'fighter{card_id}'][2]+=zavoj
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +18 health")
            elif number>300 and number<351:
                fighters[f'fighter{card_id}'][5]+=stit
                fighters[f'fighter{card_id}'][2]+=stit
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +4 deffence")
            elif number>350 and number<401:
                fighters[f'fighter{card_id}'][5]+=oklop
                fighters[f'fighter{card_id}'][2]+=oklop
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +6 deffence")
            elif number>400 and number<451:
                fighters[f'fighter{card_id}'][4]+=mac
                fighters[f'fighter{card_id}'][2]+=mac
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +6 attack")
            elif number>450 and number<501:
                fighters[f'fighter{card_id}'][4]+=dupli_mac
                fighters[f'fighter{card_id}'][2]+=dupli_mac
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +10 attack")
            elif number>500 and number<551:
                fighters[f'fighter{card_id}'][3]+=boks
                fighters[f'fighter{card_id}'][2]+=boks
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -12 health")
            elif number>550 and number<601:
                fighters[f'fighter{card_id}'][3]+=boks_crveni
                fighters[f'fighter{card_id}'][2]+=boks_crveni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -18 health")
            elif number>600 and number<651:
                fighters[f'fighter{card_id}'][5]+=knock
                fighters[f'fighter{card_id}'][2]+=knock
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -4 deffence")
            elif number>650 and number<701:
                fighters[f'fighter{card_id}'][5]+=knock_crveni
                fighters[f'fighter{card_id}'][2]+=knock_crveni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -6 deffence")
            elif number>700 and number<751:
                fighters[f'fighter{card_id}'][4]+=zvijezde
                fighters[f'fighter{card_id}'][2]+=zvijezde
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -6 attack")
            elif number>750 and number<801:
                fighters[f'fighter{card_id}'][4]+=zvijezde_crvene
                fighters[f'fighter{card_id}'][2]+=zvijezde_crvene
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -10 attack")
            elif number>800 and number<834:
                fighters[f'fighter{card_id}'][4]+napitak_crveni
                fighters[f'fighter{card_id}'][2]+=napitak_crveni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +14 attack")
            elif number>833 and number<867:
                fighters[f'fighter{card_id}'][5]+=napitak_plavi
                fighters[f'fighter{card_id}'][2]+=napitak_plavi
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +8 deffence")
            elif number>866 and number<900:
                fighters[f'fighter{card_id}'][3]+=napitak_zeleni
                fighters[f'fighter{card_id}'][2]+=napitak_zeleni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +24 health")
            elif number>899 and number<934:
                fighters[f'fighter{card_id}'][4]+=napitak_crvenocrni
                fighters[f'fighter{card_id}'][2]+=napitak_crvenocrni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -14 attack")
            elif number>933 and number<967:
                fighters[f'fighter{card_id}'][3]+=napitak_zelenocrni
                fighters[f'fighter{card_id}'][2]+=napitak_zelenocrni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -24 health")
            elif number>966 and number<1001:
                fighters[f'fighter{card_id}'][5]+=napitak_plavo_crni
                fighters[f'fighter{card_id}'][2]+=napitak_plavo_crni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -8 deffence")
            else:
                bonuses.append('not valid')
                
        return bonuses, fighters
    
    def get_random_numbers(self, request):
        if 'bonus_numbers' not in request.session:
            num_of_numbers = 32
            numbers = [random.randint(1, 1000) for _ in range(num_of_numbers)]
            request.session['bonus_numbers'] = list(numbers)
        else:
            numbers = list(request.session['bonus_numbers'])

        return numbers


"""  ######################################################################  """

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
                cards = self.get_random_cards()
                card_ids=[card.id for card in cards]
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

        random_cards=list(drawn_human_cards+drawn_fantasy_cards+drawn_creature_cards+drawn_alien_cards)

        return random_cards
    
    """  #########################################################################################  """

class Tournament_view(TemplateView):
    template_name='game/tournament.html'

    """   ########################################################################################  """

class PairsView(ListView):
    template_name='game/pairs.html'
    model=Card
    context_object_name='pairs_list'

    def get(self, request):
        if request.session['card_ids']:
            card_ids=request.session.get('card_ids')
            fighters=request.session.get('shuffled')
            if fighters:
                fighters=request.session.get('shuffled')
            else:
                fighters=self.get_pairs(request)

        cards=Card.objects.filter(id__in=card_ids)
        context={'fighters':fighters, 'cards':cards}
        return render(request, self.template_name, context)


    def get_pairs(self, request):
        bonus_view=Bonus_view()
        bonuses, fighters=bonus_view.define_bonuses(request)
        keys=list(fighters.keys())
        random.shuffle(keys)
        shuffled_dict= {key: fighters[key] for key in keys}
        request.session['shuffled']=shuffled_dict
        return shuffled_dict
    

