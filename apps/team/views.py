from django.views.generic import DetailView

from apps.team.models import Team


class TeamDetailView(DetailView):
    model = Team
    pk_url_kwarg = 'country_code'
    context_object_name = 'team'
    template_name = 'team-detail.html'

