from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView


class HomeView(RedirectView):
    url = reverse_lazy('ranking')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def robots_txt(request):
    lines = [
        'User-Agent: *',
        'Disallow: /admin/',
        'Allow: /\n',
        'Sitemap: https://rankfoot.com/sitemap.xml'
    ]
    return HttpResponse(
        content='\n'.join(lines),
        content_type='text/plain'
    )


def ads_txt(request):
    return HttpResponse(
        content='google.com, pub-7212047264593114, DIRECT, f08c47fec0942fa0',
        content_type='text/plain'
    )
