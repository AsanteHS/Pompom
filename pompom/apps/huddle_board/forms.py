from django import forms
from django.utils.translation import ugettext as _

from pompom.apps.huddle_board.models import CardNote, SiteConfiguration


class ObservationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        sections = kwargs.pop('sections')
        super().__init__(*args, **kwargs)
        for section in sections:
            field_name = 'observation_{}'.format(section.id)
            self.fields[field_name] = forms.NullBooleanField()
            self.fields[field_name].section = section.id


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

    def clean(self):
        cleaned_data = super().clean()
        entered_password = cleaned_data.get("password")
        board_passwords = SiteConfiguration.get_board_passwords()
        if board_passwords and entered_password not in board_passwords:
            raise forms.ValidationError("Enter a valid password.")
        return cleaned_data
