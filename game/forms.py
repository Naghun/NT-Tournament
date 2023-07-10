from django import forms

class SaveGame(forms.Form):
    
    save_name=forms.CharField(max_length=100)

class World_name(forms.Form):
    
    world_name=forms.CharField(max_length=100)