from django import forms

from apps.ranking.models import Team


class TeamChangeForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'flag_url', 'confederation', 'api_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'py-1 border-dark-subtle'}),
            'flag_url': forms.TextInput(attrs={'class': 'py-1 border-dark-subtle'}),
            'confederation': forms.Select(attrs={'class': 'py-1 border-dark-subtle'}),
            'api_id': forms.TextInput(attrs={'class': 'py-1 border-dark-subtle'}),
        }
