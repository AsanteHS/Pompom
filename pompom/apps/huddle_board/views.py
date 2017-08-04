from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, RedirectView, DetailView

from pompom.apps.huddle_board.forms import ObservationForm
from pompom.apps.huddle_board.models import Card, Observation, Answer, Board


class HomeView(RedirectView):
    url = reverse_lazy('pompom:huddle_board', args=[Board.objects.first().id])


class HuddleBoardView(TemplateView):
    template_name = 'huddle_board/huddle_board.html'

    def __init__(self):
        super().__init__()
        self.board = Board.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        return super().get_context_data(board=self.board, **kwargs)


class MobileMenuView(DetailView):
    model = Board
    template_name = 'huddle_board/mobile_menu.html'


class PerformObservationView(FormView):
    template_name = 'huddle_board/observation.html'
    form_class = ObservationForm

    def __init__(self):
        super().__init__()
        self.board = None
        self.card = None
        self.sections = None
        self.gradable_sections = None

    def get(self, request, *args, **kwargs):
        self.get_board()
        self.card = self.board.draw_card()
        self.parse_card()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.get_board()
        self.card = Card.objects.get(id=request.POST['card'])
        self.parse_card()
        return super().post(request, *args, **kwargs)

    def get_board(self):
        self.board = Board.objects.get(id=self.kwargs['pk'])

    def parse_card(self):
        self.sections = self.card.sections.all()
        self.gradable_sections = self.sections.filter(is_gradable=True)

    def get_success_url(self):
        return reverse_lazy('pompom:mobile_menu', args=[self.board.id])

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
