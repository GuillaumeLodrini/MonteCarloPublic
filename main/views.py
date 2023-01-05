from django.shortcuts import render
from django.views.generic import FormView
from .forms import InputForm
from .utils import get_results
import urllib, base64
class IndexTemplateView(FormView):
    template_name = 'main/index.html'
    form_class = InputForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['form'] = kwargs.get('form', InputForm())
        context['uri1'] = kwargs.get('uri1', None)
        context['uri2'] = kwargs.get('uri2', None)
        context['uri3'] = kwargs.get('uri3', None)

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        
        d1 = form.cleaned_data['d1']
        d2 = form.cleaned_data['d2']
        m1Base = form.cleaned_data['m1Base']
        m1Delta = form.cleaned_data['m1Delta']
        m2Base = form.cleaned_data['m2Base']
        m2Delta = form.cleaned_data['m2Delta']
        theta1Base = form.cleaned_data['theta1Base']
        theta1Delta = form.cleaned_data['theta1Delta']
        theta2Base = form.cleaned_data['theta2Base']
        theta2Delta = form.cleaned_data['theta2Delta']
        theta1fBase = form.cleaned_data['theta1fBase']
        theta1fDelta = form.cleaned_data['theta1fDelta']
        theta2fBase = form.cleaned_data['theta2fBase']
        theta2fDelta = form.cleaned_data['theta2fDelta']
        a1Base = form.cleaned_data['a1Base']
        a1Delta = form.cleaned_data['a1Delta']
        a2Base = form.cleaned_data['a2Base']
        a2Delta = form.cleaned_data['a2Delta']

        uri1, uri2, uri3 = get_results(d1, d2, m1Base, m1Delta, m2Base, m2Delta, theta1Base, theta1Delta, theta2Base, theta2Delta, theta1fBase, theta1fDelta, theta2fBase, theta2fDelta, 20000, a1Base, a1Delta, a2Base, a2Delta)
        return self.render_to_response(self.get_context_data(form=form, uri1=uri1, uri2=uri2, uri3=uri3))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))