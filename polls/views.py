import logging

from cities.models import Continent, Country
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from polls.models import Question

logger = logging.getLogger(__name__)


class QuestionListView(ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'polls/question_list.html'


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'polls/question_detail.html'


class QuestionCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Question
    fields = ['question_text']
    success_message = "Question created successfully!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.pub_date = timezone.now()
        return super().form_valid(form)


class QuestionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Question
    fields = ['question_text']
    template_name_suffix = '_update_form'
    success_message = 'Question updated successfully!'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.can_update(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj


class QuestionDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('polls:question_list')
    success_message = 'Question deleted successfully!'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.can_delete(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(QuestionDelete, self).delete(request, *args, **kwargs)


class VoteView(TemplateView):
    template_name = 'polls/vote.html'


class ResultsView(TemplateView):
    template_name = 'polls/results.html'


class ContinentListView(ListView):
    model = Continent
    context_object_name = 'continent_list'
    template_name = 'polls/continent_list.html'


class CountryListView(ListView):
    model = Country
    context_object_name = 'country_list'
    template_name = 'polls/country_list.html'
