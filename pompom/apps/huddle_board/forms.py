from django import forms


class ObservationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        sections = kwargs.pop('sections')
        super().__init__(*args, **kwargs)
        for section in sections:
            field_name = 'observation_{}'.format(section.id)
            self.fields[field_name] = forms.NullBooleanField()
            self.fields[field_name].section = section.id
