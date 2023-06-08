from django.urls import path
from .views import Start_view, List_view, Tournament_view, Bonus_view, Draft_view, Cards_view

urlpatterns = [
    path('', Start_view.as_view(), name='start'),
    path('list/', List_view.as_view(), name='list'),
    path('draft/', Draft_view.as_view(), name='draft'),
    path('tournament/', Tournament_view.as_view(), name='tournament'),
    path('bonus/', Bonus_view.as_view(), name='bonus'),
    path('cards/', Cards_view.as_view(), name='cards'),
]