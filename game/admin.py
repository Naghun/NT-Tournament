from django.contrib import admin
from .models import Card, InitialCards, Tournament, Winners, World


class CardAdmin(admin.ModelAdmin):
    pass

class InitialCardsAdmin(admin.ModelAdmin):
    pass

class TournamentAdmin(admin.ModelAdmin):
    pass

class WinnersAdmin(admin.ModelAdmin):
    pass

class WorldAdmin(admin.ModelAdmin):
    pass

admin.site.register(Card, CardAdmin)
admin.site.register(InitialCards, InitialCardsAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Winners, WinnersAdmin)
admin.site.register(World, WorldAdmin)

