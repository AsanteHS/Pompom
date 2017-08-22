from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView, CreateView

from pompom.apps.huddle_board.forms import ObservationForm, CardNoteForm
from pompom.apps.huddle_board.models import Card, Observation, Answer, Board, CardNote, SafetyMessage
from pompom.libs.tokens import MobileToken


class HomeView(TemplateView):
    template_name = 'huddle_board/home.html'

    def get_context_data(self, **kwargs):
        boards = Board.objects.all()
        return super().get_context_data(boards=boards, **kwargs)


class HuddleBoardView(TemplateView):
    template_name = 'huddle_board/huddle_board.html'

    def get_context_data(self, **kwargs):
        board = get_object_or_404(Board, id=self.kwargs['pk'])
        return super().get_context_data(
            board=board,
            graded_cards=board.latest_graded_cards(),
            result_history=board.result_history(),
            token=MobileToken().ciphertext,
            safety_message=SafetyMessage.objects.first(),
            **kwargs
        )


class TokenRequiredMixin(UserPassesTestMixin):

    login_url = reverse_lazy('pompom:unauthorized')
    redirect_field_name = None

    def test_func(self):
        token = MobileToken(self.kwargs['token'])
        return token.is_valid()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'token' not in context:
            context['token'] = self.kwargs['token']
        return context


class MobileMenuView(TokenRequiredMixin, DetailView):
    model = Board
    template_name = 'huddle_board/mobile_menu.html'


class ChooseCardView(TokenRequiredMixin, TemplateView):
    template_name = 'huddle_board/choose_card.html'

    def get_context_data(self, **kwargs):
        board = get_object_or_404(Board, id=self.kwargs['pk'])
        cards = board.deck.cards.order_by('title') if board.deck else []
        return super().get_context_data(board=board, cards=cards, **kwargs)


class PerformObservationView(TokenRequiredMixin, FormView):
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
        self.validate_card_exists_in_deck()
        self.parse_card()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.get_board()
        self.card = Card.objects.get(id=request.POST['card'])
        self.validate_card_exists_in_deck()
        self.parse_card()
        return super().post(request, *args, **kwargs)

    def get_board(self):
        self.board = get_object_or_404(Board, id=self.kwargs['pk'])

    def pick_card(self, request):
        card_id = request.GET.get('card')
        self.card = self.cherry_picked_card(card_id) or self.board.draw_card()

    def cherry_picked_card(self, card_id):
        if card_id is None:
            return None
        return get_object_or_404(Card, id=card_id)

    def validate_card_exists_in_deck(self):
        get_object_or_404(self.board.deck.cards, id=self.card.id)

    def parse_card(self):
        self.sections = self.card.sections.all()
        self.gradable_sections = self.sections.filter(is_gradable=True)

    def get_success_url(self):
        return reverse_lazy('pompom:mobile_menu', args=[self.board.id, self.kwargs['token']])

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


class AddCardNoteView(TokenRequiredMixin, CreateView):
    model = CardNote
    form_class = CardNoteForm
    template_name = "huddle_board/card_note.html"

    def get_success_url(self):
        return reverse_lazy('pompom:mobile_menu', args=[self.kwargs['pk'], self.kwargs['token']])

    def get_context_data(self, **kwargs):
        board = get_object_or_404(Board, id=self.kwargs['pk'])
        latest_cards = board.latest_distinct_cards(amount=3)
        return super().get_context_data(board=board, latest_cards=latest_cards, **kwargs)

    def form_valid(self, form):
        form.instance.board_id = self.kwargs['pk']
        return super().form_valid(form)


class UnauthorizedView(TemplateView):
    template_name = 'huddle_board/unauthorized.html'
