from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import Card
import random
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin

# Create your views here.

class TournamentMixin(AccessMixin):
    def redirect_user(self, request, *args, **kwargs):
        if 'card_ids' not in request.session:
            return redirect(reverse('start'))
        elif 'bonus_numbers' not in request.session:
            return redirect(reverse('bonus'))
        elif 'shuffled' not in request.session:
            return redirect(reverse('pairs'))
        else:
            return super().get(request, *args, **kwargs)



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
            
            if 'shuffled' in request.session:
                del request.session['shuffled']
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


"""  ######################################################################  """

class Bonus_view(TournamentMixin, ListView):
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
                fighters[f'fighter{card_id}'][4]+=napitak_crveni
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
    
    """  #########################################################################################  """

    
class PairsView(TournamentMixin, ListView):
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

    """   ########################################################################################  """
    
class Tournament_view(TournamentMixin, ListView):
    template_name='game/tournament.html'
    model=Card
    context_object_name='tournament_list'

    def get(self, request):
        fighters = request.session.get('shuffled')
        context = {'fighters': fighters}
        return render(request, self.template_name, context)
        

    def post(self, request):

        if 'round1' in request.POST:
            logs_round1, round1_winnners=self.round1(request)
            context={'round1_logs': logs_round1, 'round1':round1_winnners}
            return render(request, self.template_name, context)
        
        elif 'round16' in request.POST:
            logs_round16, round16_winners=self.round_of_16(request)
            context={'round16_logs': logs_round16, 'round16':round16_winners}
            return render(request, self.template_name, context)
        
        elif 'quarters' in request.POST:
            logs_quarters, quarters_winners=self.quarters(request)
            context={'quarters_logs': logs_quarters, 'quarters':quarters_winners}
            return render(request, self.template_name, context)
        
        elif 'semis' in request.POST:
            logs_semis, semis_winners=self.semi_finals(request)
            context={'semis_logs': logs_semis, 'semis':semis_winners}
            return render(request, self.template_name, context)
        
        elif 'finals' in request.POST:
            logs_finals, winner=self.finals(request)
            card_ids=request.session.get('card_ids')
            cards=Card.objects.filter(id__in=card_ids)
            context={'finals_logs': logs_finals, 'finals':winner, 'cards':cards}
            return render(request, self.template_name, context)
        elif 'end_tournament' in request.POST:
            del request.session['card_ids']
            del request.session['bonus_numbers']
            del request.session['shuffled']
            cards=[]
            numbers=[]
            request.session.modified=True
            return redirect(reverse('start'))

    
    def round1(self, request):
        fighters=request.session.get('shuffled')
        logs, winners=self.fight(fighters)
        return logs, winners
    
    def round_of_16(self, request):
        nothing, fighters = self.round1(request)
        logs, winners=self.fight(fighters)
        return logs, winners
    
    def quarters(self, request):
        nothing, fighters = self.round_of_16(request)
        logs, winners=self.fight(fighters)
        return logs, winners
    
    def semi_finals(self, request):
        nothing, fighters = self.quarters(request)
        logs, winners=self.fight(fighters)
        return logs, winners
    
    def finals(self, request):
        nothing, fighters = self.semi_finals(request)
        logs, winners=self.fight(fighters)
        return logs, winners



    def fight(self, fighters):
        fighters=fighters
        num_fighters = len(fighters)
        log=[]
        winners={}

        for i in range(0, num_fighters-1, 2):
            f1 = list(fighters.values())[i]
            f2 = list(fighters.values())[i+1]
            num_of_fight=int((i/2)+1)

            f1_id=f1[0]
            f1_name=f1[1]
            f1_overall=f1[2]
            f1_hp=f1[3]
            f1_att=f1[4]
            f1_deff=f1[5]

            f2_id=f2[0]
            f2_name=f2[1]
            f2_overall=f2[2]
            f2_hp=f2[3]
            f2_att=f2[4]
            f2_deff=f2[5]

            round=0

            log.append(f'Fight {num_of_fight}: {f1_name} vs {f2_name}')
            log.append(f'--------------------------------------------')
            log.append(f'Stats:')
            log.append(f'{f1_name}: Overall: {f1_overall} Hp: {f1_hp} Att: {f1_att} Deff: {f1_deff}')
            log.append(f'{f2_name}: Overall: {f2_overall} Hp: {f2_hp} Att: {f2_att} Deff: {f2_deff}')

            while round < 20 and f1_hp > 0 and f2_hp > 0: 
                round+=1
                log.append(f'----------------')
                log.append(f'Round{round} starts!')

                if f1_att<=f2_deff and f2_att<=f1_deff:
                    f2_hp=0
                    f1_hp=int(f1_hp/2)
                    f1_att=int(f1_hp/2)
                    f1_deff=int(f1_hp/2)
                    f1_overall=f1_hp+f1_att+f1_deff
                    log.append(f'Both fighters have stronger armor than enemy attack, luck of draw decided the winner is {f1_name}')
                    break
                elif f1_att<=f2_deff:
                    f2_hp=f2_hp
                    f1_hp=0
                    log.append(f'{f1_name} has lower attack {f1_att} than {f2_name} deff {f2_deff} so the winner with full hp is {f2_name}')
                    break
                elif f2_att<=f1_deff:
                    f1_hp=f1_hp
                    f2_hp=0
                    log.append(f'{f2_name} has lower attack {f2_att} than {f1_name} deff {f1_deff} so the winner with full hp is {f1_name}')
                    break
                else:
                    f2_hp-=f1_att-f2_deff
                    log.append(f'{f1_name} attacks. {f1_att} attack damage - {f2_deff} damage blocked = {f1_att-f2_deff} damage dealt')
                    log.append(f'{f2_name} health left: {f2_hp}')
                    if f2_hp<=0:
                        f2_hp=0
                        log.append(f'{f2_name} died')
                        f1_overall=f1_hp+f1_att+f1_deff
                        break

                    f1_hp-=f2_att-f1_deff
                    log.append(f'{f2_name} attacks. {f2_att} attack damage - {f1_deff} damage blocked = {f2_att-f1_deff} damage dealt')
                    log.append(f'{f1_name} health left: {f1_hp}')
                    if f1_hp<=0:
                        f1_hp=0
                        log.append(f'{f1_name} died')
                        f2_overall=f2_hp+f2_att+f2_deff
                        break
            if f1_hp > 0:
                log.append(f'{f1_name} health left: {f1_hp}.')
                log.append(f'')

            elif f2_hp > 0:
                log.append(f'{f2_name} health left: {f2_hp}')
                log.append(f'')

            if f1_hp > 0:
                Round1_winner = [f1_id, f1_name, f1_overall, f1_hp, f1_att, f1_deff]
            elif f2_hp > 0:
                Round1_winner = [f2_id, f2_name, f2_overall, f2_hp, f2_att, f2_deff]

            winners[f"round1_winner{num_of_fight}"] = Round1_winner

            log.append(f'Fight {num_of_fight} winner: {Round1_winner[1]}')
            log.append('-------------------------------------------------')
            log.append('')
            log.append('')

        return log, winners