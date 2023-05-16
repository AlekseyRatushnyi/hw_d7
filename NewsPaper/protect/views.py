from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _  # импортируем функцию для перевода


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context





# Create your views here.

class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)