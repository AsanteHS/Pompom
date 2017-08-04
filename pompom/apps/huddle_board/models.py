import random

from bs4 import BeautifulSoup
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from ordered_model.models import OrderedModel


class Card(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))

    def __str__(self):
        return self.title


class CardSection(OrderedModel):
    contents = RichTextField(verbose_name=_('contents'))
    card = models.ForeignKey(Card, related_name=_('sections'), verbose_name=_('card'))
    is_gradable = models.BooleanField(verbose_name=_('is gradable'))

    order_with_respect_to = 'card'

    def __str__(self):
        if not self.contents:
            return super().__str__()
        soup = BeautifulSoup(self.contents, "html.parser")
        title = soup.find().text
        return title[:50]


class Deck(TitleDescriptionModel):
    cards = models.ManyToManyField(Card, blank=True, related_name=_('decks'), verbose_name=_('cards'))

    def __str__(self):
        return self.title


class Board(TitleDescriptionModel):
    deck = models.ForeignKey(Deck, blank=True, null=True, verbose_name=_('deck'))
    draw_pile = models.ManyToManyField(Card, blank=True, verbose_name=_('draw pile'))

    def __str__(self):
        return self.title

    class ShuffleException(Exception):
        pass

    def draw_card(self):
        pile_count = self.draw_pile.count()
        if not pile_count:
            self.reshuffle()
            pile_count = self.draw_pile.count()
        drawn_card = self.pick_random_card(pile_count)
        self.draw_pile.remove(drawn_card)
        return drawn_card

    def pick_random_card(self, pile_count):
        random_index = random.randrange(pile_count)
        return self.draw_pile.all()[random_index]

    def reshuffle(self):
        if not self.deck:
            raise self.ShuffleException("Cannot perform shuffle; board has no deck assigned.")
        cards_in_deck = self.deck.cards.all()
        if not cards_in_deck:
            raise self.ShuffleException("Cannot perform shuffle; assigned deck has no cards.")
        self.draw_pile.set(cards_in_deck)


class Observation(TimeStampedModel):
    pass


class Answer(models.Model):
    GRADES = ((True, 'Pass'), (False, 'Fallout'), (None, 'N/A'))

    observation = models.ForeignKey(Observation, related_name=_('answers'), verbose_name=_('observation'))
    card_section = models.ForeignKey(CardSection, related_name=_('answers'), verbose_name=_('card section'))
    grade = models.NullBooleanField(choices=GRADES)

    def __str__(self):
        return ', '.join([str(self.observation), str(self.card_section), str(self.grade)])
