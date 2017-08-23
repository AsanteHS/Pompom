from django import forms
from django.contrib import admin
from ordered_model.admin import OrderedTabularInline

from pompom.apps.huddle_board.models import Card, CardSection, Observation, Answer, Board, Deck, CardNote, SafetyMessage


class CardSectionInline(OrderedTabularInline):
    model = CardSection
    fields = ('title', 'contents', 'is_gradable', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'title':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


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
    fields = ('created', 'board', 'card')
    readonly_fields = ('created',)
    inlines = (AnswerInline, )
    list_display = ('id', 'card', 'board', 'created')
    list_filter = ('card', 'board', 'created')


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'deck')


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'boards_using_this_deck')
    readonly_fields = ('boards_using_this_deck', )
    filter_horizontal = ('cards', )

    def boards_using_this_deck(self, deck):
        return ", ".join([self.board_url(board) for board in deck.board_set.all()]) or "-"
    boards_using_this_deck.allow_tags = True

    def board_url(self, board):
        return '<a href="/admin/huddle_board/board/{id}">{title}</a>'.format(id=board.id, title=board.title)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('board_set')


@admin.register(CardNote)
class CardNoteAdmin(admin.ModelAdmin):
    list_display = ('to_string', 'card', 'board', 'created')
    list_filter = ('card', 'board', 'created')

    def to_string(self, obj):
        return str(obj)
    to_string.short_description = 'Contents'


@admin.register(SafetyMessage)
class SafetyMessageAdmin(admin.ModelAdmin):
    list_display = ('to_string', 'created', 'modified')

    def to_string(self, obj):
        return str(obj)
    to_string.short_description = 'Contents'
