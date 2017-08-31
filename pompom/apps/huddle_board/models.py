import random
from datetime import timedelta, datetime

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from ordered_model.models import OrderedModel
from solo.models import SingletonModel
from taggit.managers import TaggableManager

from .utils import truncate_string


MAX_CARDS_DISPLAYED = 3
MAX_GRAPHS_DISPLAYED = 10


class Card(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    companion_image = models.ImageField(upload_to='companion_images/', blank=True, null=True,
                                        verbose_name=_('companion image'))
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def tag_list(self):
        return ", ".join(tag.name for tag in self.tags.all())

    def title_and_tags(self):
        tags = " ".join(['[{name}]'.format(name=tag.name) for tag in self.tags.all()])
        return " ".join([self.title, tags])


class CardSection(OrderedModel):
    title = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('title'))
    contents = RichTextField(blank=True, null=True, verbose_name=_('contents'))
    card = models.ForeignKey(Card, related_name='sections', verbose_name=_('card'))
    is_gradable = models.BooleanField(verbose_name=_('is gradable'))
    check_count = models.PositiveSmallIntegerField(default=1, verbose_name=_('check count'))

    order_with_respect_to = 'card'

    def __str__(self):
        return self.title or "(no title)"


class GradedCardSection:

    def __init__(self, card_section, observation):
        self.section = card_section
        self.grade = self.grade_section(observation)

    def grade_section(self, observation):
        if not observation:
            return None
        try:
            answer = observation.answers.get(card_section=self.section)
        except Answer.DoesNotExist:
            return None
        return answer.grade


class GradedCard:

    def __init__(self, observation):
        self.card = observation.card
        self.graded_sections = [GradedCardSection(section, observation) for section in self.card.sections.all()]
        self.grade = observation.grade
        self.datetime = observation.created


class Deck(TitleDescriptionModel):
    cards = models.ManyToManyField(Card, blank=True, related_name='decks', verbose_name=_('cards'))

    def __str__(self):
        return self.title


class Board(TitleDescriptionModel):
    deck = models.ForeignKey(Deck, blank=True, null=True, verbose_name=_('deck'))

    def __str__(self):
        return self.title

    class DeckException(Exception):
        pass

    def draw_card(self):
        self.validate_non_empty_deck()
        deck_size = self.deck.cards.count()
        random_index = random.randrange(deck_size)
        return self.deck.cards.all()[random_index]

    def validate_non_empty_deck(self):
        if not self.deck:
            raise self.DeckException("Cannot draw a card; board has no deck assigned.")
        if not self.deck.cards.exists():
            raise self.DeckException("Cannot draw a card; assigned deck has no cards.")

    def latest_distinct_cards(self, amount):
        """
        Return _amount_ cards from this board's deck, in descending order by datetime of last observation
        (counting observations for this board only). If there aren't enough observed cards,
        expand using unobserved cards from the deck.
        """
        if not self.deck:
            return []
        latest_cards = []
        for observation in self.observations.iterator():  # avoid fetching all observations at once
            if observation.card not in latest_cards:
                latest_cards.append(observation.card)
            if len(latest_cards) == amount:
                return latest_cards
        latest_cards += [card for card in self.deck.cards.all() if card not in latest_cards]
        return latest_cards[:amount]

    def latest_observations(self):
        return self.observations.all()[:MAX_CARDS_DISPLAYED]

    def latest_graded_cards(self):
        observations = self.latest_observations()
        return [GradedCard(observation) for observation in observations]

    def result_history(self):
        shown_cards = self.latest_distinct_cards(amount=MAX_GRAPHS_DISPLAYED)
        return self.history_graph(shown_cards)

    def history_graph(self, cards):
        graph = []
        for card in cards:
            grades = self.historic_grades(card)
            graph_row = (card, grades, self.success_rate(grades))
            graph.append(graph_row)
        return graph

    def historic_grades(self, card):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        card_observations = self.observations.filter(card=card, created__gte=thirty_days_ago).order_by('created')
        return [observation.grade() for observation in card_observations]

    def success_rate(self, grades):
        if not grades:
            return None
        return grades.count(True) / float(len(grades))


class Observation(TimeStampedModel):
    board = models.ForeignKey(Board, related_name='observations', verbose_name=_('board'))
    card = models.ForeignKey(Card, related_name='observations', verbose_name=_('card'))

    def grade(self):
        answer_grades = {answer.grade for answer in self.answers.all()}
        if False in answer_grades:
            return False
        if True in answer_grades:
            return True
        return None


class Answer(models.Model):
    GRADES = ((True, 'Pass'), (False, 'Fallout'), (None, 'N/A'))

    observation = models.ForeignKey(Observation, related_name='answers', verbose_name=_('observation'))
    card_section = models.ForeignKey(CardSection, related_name='answers', verbose_name=_('card section'))
    grade = models.NullBooleanField(choices=GRADES)

    def __str__(self):
        return ', '.join([str(self.observation), str(self.card_section), str(self.grade)])


class CardNote(TimeStampedModel):
    contents = models.TextField(verbose_name=_('contents'))
    board = models.ForeignKey(Board, related_name='notes', verbose_name=_('board'))
    card = models.ForeignKey(Card, related_name='notes', verbose_name=_('card'))

    def __str__(self):
        return truncate_string(self.contents)


class SafetyMessage(TimeStampedModel):
    contents = RichTextField(verbose_name=_('contents'))

    def __str__(self):
        return truncate_string(self.contents, max_length=100)


class SiteConfiguration(SingletonModel):
    board_passwords = models.TextField(
        blank=True,
        verbose_name=_('huddle board passwords'),
        help_text=_('Multiple comma-separated values are allowed.'),
    )

    def __str__(self):
        return "Site Configuration"

    @classmethod
    def get_board_passwords(cls):
        config = cls.get_solo()
        return {password.strip() for password in config.board_passwords.split(',') if password.strip()}
