from django import forms

class SaveGame(forms.Form):
    slot_choices= [
        ('1', 'Slot 1'),
        ('2', 'Slot 2'),
        ('3', 'Slot 3'),
        ('4', 'Slot 4'),
    ]

    slot = forms.ChoiceField(choices=slot_choices)
    save_name=forms.CharField(max_length=100)