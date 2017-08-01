from django.contrib import admin

from pompom.apps.huddle_board.models import Card, CardSection, Observation, Answer

admin.site.register(Card)
admin.site.register(CardSection)
admin.site.register(Observation)
admin.site.register(Answer)
