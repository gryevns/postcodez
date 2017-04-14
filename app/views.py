import django_rq

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView
from django.views.generic.edit import FormView

from app import forms, tasks, models


class IndexView(FormView):
    form_class = forms.PostcodeForm
    template_name = 'index.html'
    success_url = '/'

    def form_valid(self, form):
        postcodes = form.cleaned_data['postcodes']
        models.Postcode.objects.all().delete()
        queryset = models.Postcode.objects.bulk_create([
            models.Postcode(postcode=postcode) for postcode in postcodes
        ])
        for obj in queryset:
            tasks.process.delay(obj.postcode, clean=form.cleaned_data['clean'])
        return super(IndexView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['postcodes_exist'] = models.Postcode.objects.exists()
        context['postcodes'] = models.Postcode.objects.filter(deleted=False)
        context['progress'] = models.Postcode.objects.progress()
        context['invalid'] = models.Postcode.objects.invalid().count()
        return context


class ClearView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        django_rq.get_queue().empty()
        models.Postcode.objects.all().delete()
        return super(ClearView, self).get_redirect_url(*args, **kwargs)
