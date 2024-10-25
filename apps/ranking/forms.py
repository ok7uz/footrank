from django import forms

from apps.game.models import Competition


class CompetitionChangeForm(forms.ModelForm):

    class Meta:
        model = Competition
        fields = ['league', 'round', 'coefficient']
        widgets = {
            'league': forms.Select(attrs={'class': 'py-1 border-dark-subtle'}),
            'round': forms.TextInput(attrs={'class': 'py-1 border-dark-subtle'}),
            'coefficient': forms.TextInput(attrs={'class': 'py-1 border-dark-subtle'}),
        }
