from django.contrib import admin
from ordered_model.admin import OrderedTabularInline

from pompom.apps.huddle_board.models import Card, CardSection, Observation, Answer, Board, Deck


class CardSectionInline(OrderedTabularInline):
    model = CardSection
    fields = ('contents', 'is_gradable', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    inlines = (CardSectionInline, )

    def get_urls(self):
        urls = super().get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('card_section', 'grade', )
    extra = 0


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    fields = ('created',)
    readonly_fields = ('created',)
    inlines = (AnswerInline, )
    list_display = ('id', 'created',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'deck')


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
