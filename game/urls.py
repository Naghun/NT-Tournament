from django.urls import path
from .views import Start_view, List_view, Tournament_view, Bonus_view, Draft_view, Cards_view, PairsView, Lobby_view, New_game_view, Save_game_view, Load_game_view

urlpatterns = [
    path('', Start_view.as_view(), name='start'),
    path('list/', List_view.as_view(), name='list'),
    path('draft/', Draft_view.as_view(), name='draft'),
    path('tournament/', Tournament_view.as_view(), name='tournament'),
    path('bonus/', Bonus_view.as_view(), name='bonus'),
    path('cards/', Cards_view.as_view(), name='cards'),
    path('pairs/', PairsView.as_view(), name='pairs'),
    path('delete_cards/', Draft_view.as_view(), name='delete_cards'),
    path('lobby/', Lobby_view.as_view(), name='lobby'),
    path('new_game/', New_game_view.as_view(), name='new_game'),
    path('save_game/', Save_game_view.as_view(), name='save_game'),
    path('load_game/', Load_game_view.as_view(), name='load_game'),
]