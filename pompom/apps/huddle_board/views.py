from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, RedirectView, DetailView

from pompom.apps.huddle_board.forms import ObservationForm
from pompom.apps.huddle_board.models import Card, Observation, Answer, Board


class HomeView(RedirectView):
    url = reverse_lazy('pompom:huddle_board')


class HuddleBoardView(TemplateView):
    template_name = 'huddle_board/huddle_board.html'


class MobileMenuView(DetailView):
    model = Board
    template_name = 'huddle_board/mobile_menu.html'


class PerformObservationView(FormView):
    template_name = 'huddle_board/observation.html'
    success_url = reverse_lazy('pompom:success')
    form_class = ObservationForm

    def __init__(self):
        super().__init__()
        self.card = Card.objects.first()
        self.sections = self.card.sections.all()
        self.gradable_sections = self.sections.filter(is_gradable=True)

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'sections': self.gradable_sections}

    def get_context_data(self, **kwargs):
        return super().get_context_data(card=self.card, sections=self.sections, **kwargs)

    def form_valid(self, form):
        self.save_observation(form.cleaned_data)
        return super().form_valid(form)

    def save_observation(self, submission):
        observation = Observation.objects.create()
        for section in self.gradable_sections:
            Answer.objects.create(
                observation=observation,
                card_section=section,
                grade=submission['observation_{}'.format(section.id)],
            )


class SuccessView(TemplateView):
    template_name = 'huddle_board/thanks.html'
