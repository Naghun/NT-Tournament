from django import forms

class SaveGame(forms.Form):
    
    save_name=forms.CharField(max_length=100)