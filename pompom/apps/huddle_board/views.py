from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView, CreateView, ListView

from pompom.apps.huddle_board.forms import ObservationForm, CardNoteForm
from pompom.apps.huddle_board.models import Card, Observation, Answer, Board, CardNote


class HomeView(TemplateView):
    template_name = 'huddle_board/home.html'

    def get_context_data(self, **kwargs):
        boards = Board.objects.all()
        return super().get_context_data(boards=boards, **kwargs)


class HuddleBoardView(TemplateView):
    template_name = 'huddle_board/huddle_board.html'

    def get_context_data(self, **kwargs):
        board = Board.objects.get(id=self.kwargs['pk'])
        return super().get_context_data(
            board=board,
            graded_cards=board.latest_graded_cards(),
            result_history=board.result_history(),
            **kwargs
        )


class MobileMenuView(DetailView):
    model = Board
    template_name = 'huddle_board/mobile_menu.html'


class ChooseCardView(TemplateView):
    template_name = 'huddle_board/choose_card.html'

    def get_context_data(self, **kwargs):
        board = Board.objects.get(id=self.kwargs['pk'])
        cards = board.deck.cards.order_by('title') if board.deck else []
        return super().get_context_data(board=board, cards=cards, **kwargs)


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
        self.pick_card(request)
        self.parse_card()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.get_board()
        self.card = Card.objects.get(id=request.POST['card'])
        self.parse_card()
        return super().post(request, *args, **kwargs)

    def get_board(self):
        self.board = Board.objects.get(id=self.kwargs['pk'])

    def pick_card(self, request):
        card_id = request.GET.get('card')
        cherry_picked_card = Card.objects.get(id=card_id) if card_id is not None else None
        self.card = cherry_picked_card or self.board.draw_card()

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
        observation = Observation.objects.create(
            board=self.board,
            card=self.card,
        )
        for section in self.gradable_sections:
            Answer.objects.create(
                observation=observation,
                card_section=section,
                grade=submission['observation_{}'.format(section.id)],
            )


class AddCardNoteView(CreateView):
    model = CardNote
    form_class = CardNoteForm
    template_name = "huddle_board/card_note.html"

    def get_success_url(self):
        return reverse_lazy('pompom:mobile_menu', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        board = Board.objects.get(id=self.kwargs['pk'])
        return super().get_context_data(board=board, **kwargs)

    def form_valid(self, form):
        form.instance.board_id = self.kwargs['pk']
        return super().form_valid(form)
