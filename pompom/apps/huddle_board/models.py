from bs4 import BeautifulSoup
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
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


class Observation(TimeStampedModel):
    pass


class Answer(models.Model):
    GRADES = ((True, 'Pass'), (False, 'Fallout'), (None, 'N/A'))

    observation = models.ForeignKey(Observation, related_name=_('answers'), verbose_name=_('observation'))
    card_section = models.ForeignKey(CardSection, related_name=_('answers'), verbose_name=_('card section'))
    grade = models.NullBooleanField(choices=GRADES)

    def __str__(self):
        return ', '.join([str(self.observation), str(self.card_section), str(self.grade)])
