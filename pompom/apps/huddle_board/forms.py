from django import forms
from django.utils.translation import ugettext as _
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from pompom.apps.huddle_board.models import CardNote, Card, Deck


class ObservationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        sections = kwargs.pop('sections')
        super().__init__(*args, **kwargs)
        for section in sections:
            field_name = 'observation_{}'.format(section.id)
            self.fields[field_name] = forms.NullBooleanField()
            self.fields[field_name].section = section.id


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = TagField(required=False, widget=LabelWidget)


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cards'].label_from_instance = lambda card: card.title_and_tags()


class CardNoteForm(forms.ModelForm):
    class Meta:
        model = CardNote
        fields = ('contents', 'card')
        widgets = {
            'card': forms.RadioSelect(),
            'contents': forms.Textarea(attrs={'class': 'write-card-note'}),
        }


class BoardPasswordForm(forms.Form):

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
