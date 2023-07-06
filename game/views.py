from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import Card, InitialCards, Tournament, Winners
import random, pickle
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import  LoginRequiredMixin
from .forms import SaveGame
from django.core.files.storage import default_storage

# Create your views here.

class DraftMixin:
    def dispatch(self, request, *args, **kwargs):
        if 'card_ids' not in request.session or not request.session['card_ids']:
            return redirect('draft')
        return super().dispatch(request, *args, **kwargs)
    
class BonusMixin:
    def dispatch(self, request, *args, **kwargs):
        if 'bonus_numbers' not in request.session or not request.session['bonus_numbers']:
            return redirect('bonus')
        return super().dispatch(request, *args, **kwargs)
    
class PairsMixin:
    def dispatch(self, request, *args, **kwargs):
        if 'shuffled' not in request.session or not request.session['shuffled']:
            return redirect('pairs')
        return super().dispatch(request, *args, **kwargs)


"""   ###########################################################################   """

class Start_view(LoginRequiredMixin, ListView):
    template_name='game/start.html'
    model=Tournament

    def create_new_game(self):
        tournament_data=Tournament.objects.get(id=1)
        tournament_data.tournament=1
        tournament_data.year=1
        tournament_data.save()

    def post(self, request):
        if 'new_game_button' in request.POST:
            self.create_new_game()
            return redirect('new_game')
        elif 'continue' in request.POST:
            return redirect('lobby')
        elif 'save_game_button' in request.POST:
            return redirect('save_game')
        elif 'load_game_button' in request.POST:
            return redirect('load_game')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        previous=self.request.META.get('HTTP_REFERER')

        if previous and 'lobby' in previous:
            context['from_lobby'] = True
        else:
            context['from_lobby'] = False

        return context

class List_view(ListView):
    model=Card
    template_name='game/list.html'
    context_object_name='data_of_cards'
    
class Cards_view(ListView):
    model=Card
    template_name='game/cards.html'
    context_object_name='pictures_of_cards'


"""   ##########################################################################   """

class New_game_view(LoginRequiredMixin, TemplateView):
    template_name='game/new_game_menu.html'

    def post(self, request):
        if 'world_name_button' in request.POST:
            world_name=request.POST.get('world_name')

            if world_name == '':
                message='please enter valid name'
                context={'message':message}
                return render(request, self.template_name, context)
            else:
                request.session['world_name']=world_name
                return redirect('lobby')
            

"""   ##########################################################################   """

class Load_game_view(LoginRequiredMixin, TemplateView):
    template_name='game/load_game_menu.html'
    
"""   ##########################################################################   """

class Save_game_view(LoginRequiredMixin, ListView):
    template_name='game/save_game_menu.html'
    model=Card, Tournament

    def get(self, request):
        if request.method == 'POST':
            form=SaveGame(request.POST)

            if 'save_game_button' in request.POST:
                if form.is_valid():
                    slot=form.cleaned_data['slot']
                    save_name=form.cleaned_data['save_name']
                    message='Save successful'
                    context={'message':message}
                    file_path=f'../saves/{save_name}'
                    self.save_file(file_path)
                    return redirect('lobby')
            else:
                message='something is wrong'
                form=SaveGame()
                context={'form':form, 'message':message}

        form=SaveGame()
        context={'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        if request.method == 'POST':
            form=SaveGame(request.POST)

            if 'save_game_button' in request.POST:
                if form.is_valid():
                    slot=form.cleaned_data['slot']
                    save_name=form.cleaned_data['save_name']
                    message='Save successful'
                    context={'message':message}
                    file_path=f'saves/{save_name}'
                    self.save_file(file_path)
                    return render(request, self.template_name, context)
                else:
                    message='Something is wrong'
                    form=SaveGame()
                    context={'form':form, 'message':message}

        form=SaveGame()
        context={'form':form}
        return render(request, self.template_name, context)
    
    def get_data_for_saves(self):
        tournament_data=Tournament.objects.get(id=1)
        cards=list(Card.objects.all())
        data = {
            'tournament_data': tournament_data,
            'cards': cards
        }
        return data

    def save_file(self, file_path):
        data = self.get_data_for_saves()
        with default_storage.open(file_path, 'wb') as f:
            pickle.dump(data, f)

"""   ##########################################################################   """

class Lobby_view(LoginRequiredMixin, ListView):
    model=Tournament
    template_name='game/lobby.html'

    def get(self, request):
        tournament_number=Tournament.objects.get(id=1)
        world_name=request.session.get('world_name')
        context={'tournament_number':tournament_number, 'world_name':world_name}
        return render(request, self.template_name, context)

"""  ################################################################  """
    
class Draft_view(LoginRequiredMixin, ListView):
    model=Card
    template_name='game/draft.html'
    context_object_name='draft_list'

    def get(self, request):
        card_ids = request.session.get('card_ids')
        if card_ids:
            cards = Card.objects.filter(id__in=card_ids)
        else:
            cards = []
        
        context = {'cards': cards}
        return render(request, self.template_name, context)
    
    def post(self, request):
            
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

class Bonus_view(DraftMixin, ListView):
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
        flaster=120
        zavoj=180
        napitak_zeleni=240
        boks=-120
        boks_crveni=-180
        napitak_zelenocrni=-240

        mac=20
        dupli_mac=40
        napitak_crveni=60
        zvijezde=-15
        zvijezde_crvene=-30
        napitak_crvenocrni=-45

        stit=10
        oklop=20
        napitak_plavi=30
        knock=-10
        knock_crveni=-20
        napitak_plavo_crni=-30

        grom=10
        munja=20
        napitak_narandzasti=30

        cipele=10
        cizme=15
        wound=-10
        napitak_zuti=+20
        napitak_crno_zuti=-15

        numbers=self.get_random_numbers(request)
        bonuses=[]
        card_ids=request.session.get('card_ids')
        drawn_cards=Card.objects.filter(id__in=card_ids)
        fighters={f'fighter{num+1}': 
                  [card.id, card.name, card.race, card.tier, card.overall, card.speed, card.health, card.attack, card.deffence, card.crit, card.fatique] 
                  for num, card in enumerate(drawn_cards)}
        for index, number in enumerate(numbers):
            card_id=index+1
            if number>=1 and number<=200:
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got nothing")
            elif number>200 and number<251:
                fighters[f'fighter{card_id}'][6]+=flaster
                fighters[f'fighter{card_id}'][4]+=int(flaster/10)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +120 health")
            elif number>250 and number<301:
                fighters[f'fighter{card_id}'][6]+=zavoj
                fighters[f'fighter{card_id}'][4]+=int(zavoj/10)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +180 health")
            elif number>300 and number<351:
                fighters[f'fighter{card_id}'][8]+=stit
                fighters[f'fighter{card_id}'][4]+=int(stit/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +10 deffence")
            elif number>350 and number<401:
                fighters[f'fighter{card_id}'][8]+=oklop
                fighters[f'fighter{card_id}'][4]+=int(oklop/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +20 deffence")
            elif number>400 and number<451:
                fighters[f'fighter{card_id}'][7]+=mac
                fighters[f'fighter{card_id}'][4]+=mac
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +20 attack")
            elif number>450 and number<501:
                fighters[f'fighter{card_id}'][7]+=dupli_mac
                fighters[f'fighter{card_id}'][4]+=dupli_mac
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +40 attack")
            elif number>500 and number<551:
                fighters[f'fighter{card_id}'][6]+=boks
                fighters[f'fighter{card_id}'][4]+=int(boks/10)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -120 health")
            elif number>550 and number<601:
                fighters[f'fighter{card_id}'][6]+=boks_crveni
                fighters[f'fighter{card_id}'][4]+=int(boks_crveni/10)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -180 health")
            elif number>600 and number<651:
                fighters[f'fighter{card_id}'][8]+=knock
                fighters[f'fighter{card_id}'][4]+=int(knock/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -10 deffence")
            elif number>650 and number<701:
                fighters[f'fighter{card_id}'][8]+=knock_crveni
                fighters[f'fighter{card_id}'][4]+=int(knock_crveni/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -20 deffence")
            elif number>700 and number<751:
                fighters[f'fighter{card_id}'][7]+=zvijezde
                fighters[f'fighter{card_id}'][4]+=zvijezde
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -15 attack")
            elif number>750 and number<801:
                fighters[f'fighter{card_id}'][7]+=zvijezde_crvene
                fighters[f'fighter{card_id}'][4]+=zvijezde_crvene
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -30 attack")
            elif number>800 and number<834:
                fighters[f'fighter{card_id}'][7]+=napitak_crveni
                fighters[f'fighter{card_id}'][4]+=napitak_crveni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +60 attack")
            elif number>833 and number<867:
                fighters[f'fighter{card_id}'][8]+=napitak_plavi
                fighters[f'fighter{card_id}'][4]+=int(napitak_plavi/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +30 deffence")
            elif number>866 and number<900:
                fighters[f'fighter{card_id}'][6]+=napitak_zeleni
                fighters[f'fighter{card_id}'][4]+=int((napitak_zeleni/10)/3)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got +240 health")
            elif number>899 and number<934:
                fighters[f'fighter{card_id}'][7]+=napitak_crvenocrni
                fighters[f'fighter{card_id}'][4]+=napitak_crvenocrni
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -45 attack")
            elif number>933 and number<967:
                fighters[f'fighter{card_id}'][6]+=napitak_zelenocrni
                fighters[f'fighter{card_id}'][4]+=int(napitak_zelenocrni/10)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -240 health")
            elif number>966 and number<1001:
                fighters[f'fighter{card_id}'][8]+=napitak_plavo_crni
                fighters[f'fighter{card_id}'][4]+=int(napitak_plavo_crni/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -30 deffence")
            elif number>1000 and number<1101:
                fighters[f'fighter{card_id}'][9]+=grom
                fighters[f'fighter{card_id}'][4]+=int(grom/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got 10 crit chance")
            elif number>1100 and number<1201:
                fighters[f'fighter{card_id}'][9]+=munja
                fighters[f'fighter{card_id}'][4]+=int(munja/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got 20% crit chance")
            elif number>1200 and number<1301:
                fighters[f'fighter{card_id}'][5]+=cipele
                fighters[f'fighter{card_id}'][4]+=int(cipele/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got 10 speed")
            elif number>1300 and number<1401:
                fighters[f'fighter{card_id}'][5]+=cizme
                fighters[f'fighter{card_id}'][4]+=int(cizme/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got 15 speed")
            elif number>1400 and number<1501:
                fighters[f'fighter{card_id}'][5]+=wound
                fighters[f'fighter{card_id}'][4]+=int(wound/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -10 speed")
            elif number>1500 and number<1534:
                fighters[f'fighter{card_id}'][9]+=napitak_narandzasti
                fighters[f'fighter{card_id}'][4]+=int(napitak_narandzasti/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got 30% crit chance")
            elif number>1533 and number<1567:
                fighters[f'fighter{card_id}'][5]+=napitak_zuti
                fighters[f'fighter{card_id}'][4]+=int(napitak_zuti/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got 20 speed")
            elif number>1566 and number<1601:
                fighters[f'fighter{card_id}'][5]+=napitak_crno_zuti
                fighters[f'fighter{card_id}'][4]+=int(napitak_crno_zuti/2)
                bonuses.append(f"{fighters[f'fighter{index+1}'][1]} got -15 speed")
            else:
                bonuses.append('not valid')
                
        return bonuses, fighters
    
    def get_random_numbers(self, request):
        if 'bonus_numbers' not in request.session:
            num_of_numbers = 32
            numbers = [random.randint(1, 1600) for _ in range(num_of_numbers)]
            request.session['bonus_numbers'] = list(numbers)
        else:
            numbers = list(request.session['bonus_numbers'])

        return numbers
    
    """  #########################################################################################  """

    
class PairsView(DraftMixin, BonusMixin, ListView):
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
    
class Tournament_view(DraftMixin, BonusMixin, PairsMixin, ListView):
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
            tournament_number=Tournament.objects.get(id=1)
            tournament_number.increase_year()
            request.session.modified=True
            return redirect(reverse('lobby'))

    
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
            fighter1 = list(fighters.values())[i]
            fighter2 = list(fighters.values())[i+1]
            num_of_fight=int((i/2)+1)


            if fighter1[5] > fighter2[5]:
                f1=fighter1
                f2=fighter2
            else:
                f2=fighter1
                f1=fighter2

            pair=[f1, f2]
            race_bonuses, msg_race_bonus=self.apply_race_bonus(pair)
            f1=race_bonuses[0]
            f2=race_bonuses[1]

            f1_id=f1[0]
            f1_name=f1[1]
            f1_race=f1[2]
            f1_tier=f1[3]
            f1_overall=f1[4]
            f1_speed=f1[5]
            f1_hp=f1[6]
            f1_att=f1[7]
            f1_deff=f1[8]
            f1_crit=f1[9]
            f1_fat=f1[10]
            

            f2_id=f2[0]
            f2_name=f2[1]
            f2_race=f2[2]
            f2_tier=f2[3]
            f2_overall=f2[4]
            f2_speed=f2[5]
            f2_hp=f2[6]
            f2_att=f2[7]
            f2_deff=f2[8]
            f2_crit=f2[9]
            f2_fat=f2[10]

            round=0

            msg_fat_fighter1, f1_att, f1_speed=self.apply_fatigue(f1_att, f1_speed, f1_fat)
            msg_fat_fighter2, f2_att, f2_speed=self.apply_fatigue(f2_att, f2_speed, f2_fat)

            if f1_speed > f2_speed:
                fighter1=f1
            else:
                fighter1=f2

            log.append(f'Fight {num_of_fight}: {f1_name} vs {f2_name}')
            log.append(f'--------------------------------------------')
            log.append(f'{msg_race_bonus}')
            log.append(f'{f1_name} Fatigue: {f1_fat} - {msg_fat_fighter1}')
            log.append(f'{f2_name} Fatigue: {f2_fat} - {msg_fat_fighter2}')
            log.append('')
            log.append(f'Stats:')
            log.append(f'{f1_name}: Overall: {f1_overall} Race: "{f1_race}" Speed: {f1_speed} Hp: {f1_hp} Att: {f1_att} Deff: {f1_deff} Crit: {f1_crit} ')
            log.append(f'{f2_name}: Overall: {f2_overall} Race: "{f2_race}" Speed: {f2_speed} Hp: {f2_hp} Att: {f2_att} Deff: {f2_deff} Crit: {f2_crit} ')
            log.append(f'{f1_name} is faster and attacks first.')

            while round < 30 and f1_hp > 0 and f2_hp > 0: 
                round+=1
                if round<8:
                    fatigue=0
                elif round>=7 and round<=12:
                    fatigue=1
                elif round>=13 and round<=18:
                    fatigue=2
                elif round>=19 and round<=25:
                    fatigue=3
                elif round>=20:
                    fatigue=4

                log.append(f'----------------')
                log.append(f'Round{round}:')

                # in case that f1 has crit but f2 no crit
                if f1_crit>0 and f2_crit==0:

                    f1_catt, msg_crit1=self.check_crit(f1_att, f1_crit)
                    f2_hp-=int(f1_catt*((100-f2_deff)/100))
                    log.append(f'{f1_name} has {f1_catt} attack damage {msg_crit1}, {f2_name} has {f2_deff}% deffence = {int(f1_catt*((100-f2_deff)/100))} damage dealt')
                    log.append(f'{f2_name} health left: {int(f2_hp)}')
                    f1_catt=f1_att

                    if f2_hp<=0:
                        f2_hp=0
                        log.append(f'{f2_name} died')
                        f1_overall=int((f1_att+f1_deff+f1_speed+(f1_hp/10))/3)
                        break

                    f1_hp-=int(f2_att*((100-f1_deff)/100))
                    log.append(f'{f2_name} attacks. {f2_att} attack damage {f1_name} has {f1_deff}% deffence = {int(f2_att*((100-f1_deff)/100))} damage dealt')
                    log.append(f'{f1_name} health left: {int(f1_hp)}')

                    if f1_hp<=0:
                        f1_hp=0
                        log.append(f'{f1_name} died')
                        f2_overall=int(((f2_hp/10)+f2_att+f2_deff+f2_speed)/3)
                        break

                #f2 has crit and f1 no crit
                
                elif f2_crit>0 and f1_crit==0:

                    f2_hp-=int(f1_att*((100-f2_deff)/100))
                    log.append(f'{f1_name} has {f1_att} attack damage , {f2_name} has {f2_deff}% deffence = {int(f1_att*((100-f2_deff)/100))} damage dealt')
                    log.append(f'{f2_name} health left: {int(f2_hp)}')

                    if f2_hp<=0:
                        f2_hp=0
                        log.append(f'{f2_name} died')
                        f1_overall=int((f1_att+f1_deff+f1_speed+(f1_hp/10))/3)
                        break
                    
                    f2_catt, msg_crit2 = self.check_crit(f2_att, f2_crit)
                    f1_hp-=int(f2_catt*((100-f1_deff)/100))
                    log.append(f'{f2_name} attacks. {f2_catt} attack damage {msg_crit2}, {f1_name} has {f1_deff}% deffence = {int(f2_catt*((100-f1_deff)/100))} damage dealt')
                    log.append(f'{f1_name} health left: {int(f1_hp)}')
                    f2_catt=f2_att

                    if f1_hp<=0:
                        f1_hp=0
                        log.append(f'{f1_name} died')
                        f2_overall=int(((f2_hp/10)+f2_att+f2_deff+f2_speed)/3)
                        break

                # both fighters have crit
                elif f1_crit>0 and f2_crit>0:
                    f1_catt, msg_crit1=self.check_crit(f1_att, f1_crit)
                    f2_hp-=int(f1_catt*((100-f2_deff)/100))
                    log.append(f'{f1_name} has {f1_catt} attack damage {msg_crit1}, {f2_name} has {f2_deff}% deffence = {int(f1_catt*((100-f2_deff)/100))} damage dealt')
                    log.append(f'{f2_name} health left: {int(f2_hp)}')
                    f1_catt=f1_att

                    if f2_hp<=0:
                        f2_hp=0
                        log.append(f'{f2_name} died')
                        f1_overall=int((f1_att+f1_deff+f1_speed+(f1_hp/10))/3)
                        break

                    f2_catt, msg_crit2 = self.check_crit(f2_att, f2_crit)
                    f1_hp-=int(f2_catt*((100-f1_deff)/100))
                    log.append(f'{f2_name} attacks. {f2_catt} attack damage {msg_crit2}, {f1_name} has {f1_deff}% deffence = {int(f2_catt*((100-f1_deff)/100))} damage dealt')
                    log.append(f'{f1_name} health left: {int(f1_hp)}')
                    f2_catt=f2_att

                    if f1_hp<=0:
                        f1_hp=0
                        log.append(f'{f1_name} died')
                        f2_overall=int(((f2_hp/10)+f2_att+f2_deff+f2_speed)/3)
                        break


                #no crits in match
                else:

                    f2_hp-=int(f1_att*((100-f2_deff)/100))
                    log.append(f'{f1_name} has {f1_att} attack damage {f2_name} has {f2_deff}% deffence = {int(f1_att*((100-f2_deff)/100))} damage dealt')
                    log.append(f'{f2_name} health left: {int(f2_hp)}')
                    if f2_hp<=0:
                        f2_hp=0
                        log.append(f'{f2_name} died')
                        f1_overall=int((f1_att+f1_deff+f1_speed+(f1_hp/10))/3)
                        break

                    f1_hp-=int(f2_att*((100-f1_deff)/100))
                    log.append(f'{f2_name} attacks. {f2_att} attack damage {f1_name} has {f1_deff}% deffence = {int(f2_att*((100-f1_deff)/100))} damage dealt')
                    log.append(f'{f1_name} health left: {int(f1_hp)}')
                    if f1_hp<=0:
                        f1_hp=0
                        log.append(f'{f1_name} died')
                        f2_overall=int(((f2_hp/10)+f2_att+f2_deff+f2_speed)/3)
                        break

            if f1_hp > 0:
                log.append(f'{f1_name} health left: {f1_hp}.')
                log.append(f'')

            elif f2_hp > 0:
                log.append(f'{f2_name} health left: {f2_hp}')
                log.append(f'')

            f1_fat=fatigue
            f2_fat=fatigue


            fighter1=[f1_id, f1_name, f1_race, f1_tier, f1_overall, f1_speed, f1_hp, f1_att, f1_deff, f1_crit, f1_fat]
            fighter2=[f2_id, f2_name, f2_race, f2_tier, f2_overall, f2_speed, f2_hp, f2_att, f2_deff, f2_crit, f2_fat]
            pair=[fighter1, fighter2]
            f1, f2=self.revert_class_bonus(pair)

            fatigue=0

            if f1[6] > 0:
                Round1_winner = f1
                if f1[10] > 0:
                    log.append(f'due to fighting for long time and exhaustion, {f1_name} will get level {f1_fat} fatigue minuses')
            elif f2[6] > 0:
                Round1_winner = f2
                if f2[10] > 0:
                    log.append(f'due to fighting for long time and exhaustion, {f2_name} will get level {f2_fat} fatigue minuses')

            winners[f"round1_winner{num_of_fight}"] = Round1_winner


            log.append(f'Fight {num_of_fight} winner: {Round1_winner[1]}')
            log.append('-------------------------------------------------')
            log.append('')
            log.append('')

        return log, winners
    
    def check_crit(self, f_att, f_crit):
        crit_chance=f_crit
        f_catt=f_att
        msg=''
        
        if crit_chance==10:
            crit_number=random.randint(1,100)
            if crit_number<10:
                f_catt=f_att*1.5
                msg='-Critical hit!'
            return f_catt, msg
        elif crit_chance==20:
            crit_number=random.randint(1,100)
            if crit_number<20:
                f_catt=f_att*1.5
                msg='-Critical hit!'
            return f_catt, msg
        elif crit_chance==30:
            crit_number=random.randint(1,100)
            if crit_number<30:
                f_catt=f_att*1.5
                msg='-Critical hit!'
            return f_catt, msg

    def apply_fatigue(self, f_att, f_speed, f_fat):
        msg=''

        fatigue = f_fat
        f_att=f_att
        f_speed=f_speed

        if fatigue == 0:
            msg='Fighter has no fatigue minuses'
            f_speed = f_speed
            f_att= f_att
        elif fatigue == 1:
            f_speed *= 0.8
            f_speed=int(f_speed)
            f_att *= 0.9
            f_att=int(f_att)
            msg='Due to fatigue fighter will have 20% speed and 10% attack minuses'
        elif fatigue == 2:
            f_speed *= 0.7
            f_speed=int(f_speed)
            f_att *= 0.85
            f_att=int(f_att)
            msg='Due to fatigue fighter will have 30% speed and 15% attack minuses'
        elif fatigue == 3:
            f_speed *= 0.6
            f_speed=int(f_speed)
            f_att *= 0.8
            f_att=int(f_att)
            msg='Due to fatigue fighter will have 40% speed and 20% attack minuses'
        elif fatigue == 4:
            f_speed *= 0.5
            f_speed=int(f_speed)
            f_att *= 0.75
            f_att=int(f_att)
            msg='Due to fatigue fighter will have 50% speed and 25% attack minuses'

        return msg, f_att, f_speed
    
    def apply_race_bonus(self, pair):
        f1=pair[0]
        f2=pair[1]
        msg=''
        if f1[2]=='Human' and f2[2]=='Alien':
            f1[6]+=120
            f1[4]+=12
            msg='Human gain +120 hp bonus against Alien'
        elif f1[2]=='Alien' and f2[2]=='Fantasy':
            f1[7]+=20
            f1[4]+=20
            msg='Alien gain +20 attack bonus against Fantasy'
        elif f1[2]=='Fantasy' and f2[2]=='Creature':
            f1[8]+=30
            f1[4]+=15
            msg='Fantasy gain +30 deff bonus against Creature'
        elif f1[2]=='Creature' and f2[2]=='Human':
            f1[7]+=20
            f1[4]+=20
            msg='Creature gain +20 attack bonus against Human'
        elif f2[2]=='Human' and f1[2]=='Alien':
            f2[6]+=120
            f2[4]+=12
            msg='Human gain +120 health bonus against Alien'
        elif f2[2]=='Alien' and f1[2]=='Fantasy':
            f2[7]+=20
            f2[4]+=20
            msg='Alien gain +20 attack bonus against Fantasy'
        elif f2[2]=='Fantasy' and f1[2]=='Creature':
            f2[8]+=30
            f2[4]+=15
            msg='Fantasy gain +30 deff bonus against Creature'
        elif f2[2]=='Creature' and f1[2]=='Human':
            f2[7]+=20
            f2[4]+=20
            msg='Creature gain +20 attack bonus against Human'
        else:
            msg='No fighter gets race bonuses'

        pair1=[f1, f2]

        return pair1, msg

    def revert_class_bonus(self, pair):
        f1=pair[0]
        f2=pair[1]
        if f1[2]=='Human' and f2[2]=='Alien':
            if f1[6]<=120:
                f1[6]=1
                f1[4]-=12
            else:
                f1[6]-=120
                f1[4]-=12
        elif f1[2]=='Alien' and f2[2]=='Fantasy':
            f1[7]-=20
            f1[4]-=20
        elif f1[2]=='Fantasy' and f2[2]=='Creature':
            f1[8]-=30
            f1[4]-=15
        elif f1[2]=='Creature' and f2[2]=='Human':
            f1[7]-=20
            f1[4]-=20
        elif f2[2]=='Human' and f1[2]=='Alien':
            if f2[6]<=120:
                f2[6]=1
                f2[4]-=12
            else:
                f2[6]-=120
                f2[4]-=12
        elif f2[2]=='Alien' and f1[2]=='Fantasy':
            f2[7]-=20
            f2[4]-=20
        elif f2[2]=='Fantasy' and f1[2]=='Creature':
            f2[8]-=30
            f2[4]-=15
        elif f2[2]=='Creature' and f1[2]=='Human':
            f2[7]-=20
            f2[4]-=20



        return f1, f2
