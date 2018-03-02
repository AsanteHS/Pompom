from django import forms
from django.contrib import admin
from django.urls import reverse
from ordered_model.admin import OrderedTabularInline
from solo.admin import SingletonModelAdmin
from taggit.models import Tag
from taggit_helpers.admin import TaggitListFilter
from import_export import resources, fields
from import_export.admin import ExportActionModelAdmin
from import_export.fields import Field

from pompom.apps.huddle_board.forms import CardForm, DeckForm
from .models import Card, CardSection, Observation, Answer, Board, Deck, CardNote, SafetyMessage, SiteConfiguration

class ObservationResource(resources.ModelResource):

    class Meta:
        model = Observation
        fields = ('created', 'board', 'card')

class CardResource(resources.ModelResource):
    decks = fields.Field(column_name = 'Contained in decks')
    sections = fields.Field(column_name = 'Sections')
    title = fields.Field(column_name = 'Title')

    class Meta:
        model = Card
        fields = ('tags')

    def dehydrate_title(self, card):
        return card.title
    def dehydrate_sections(self, card):
        return ', '.join(section.title or '(no title)' for section in card.sections.all())
    def dehydrate_decks(self, card):
        return ', '.join(deck.title for deck in card.decks.all())

class AnswerResource(resources.ModelResource):
    observation = fields.Field(column_name = 'Observation')
    card_section = fields.Field(column_name = 'Card section')
    card_section_contents = fields.Field(column_name = 'Contents')
    grade = fields.Field(column_name = 'Grade')
    checks_done = fields.Field(column_name = 'Checks done')
    board = fields.Field(column_name = 'Board')
    card = fields.Field(column_name = 'Card')
    #export_order = ('id', 'price', 'author', 'name')
    class Meta:
        model = Answer
        fields = ('')
    def dehydrate_card_section_contents(self, answer):
        return answer.card_section.contents
    def dehydrate_board(self, answer):
        return answer.observation.board
    def dehydrate_observation(self, answer):
        return answer.observation
    def dehydrate_card_section(self, answer):
        return answer.card_section
    def dehydrate_grade(self,answer):
        grade = { True: 'Pass', False: 'Fallout', None: 'N/A' }
        return grade[answer.grade]
    def dehydrate_checks_done(self, answer):
        return answer.checks_done
    def dehydrate_card(self, answer):
        return answer.observation.card.title


class SafetyMessageResource(resources.ModelResource):

    class Meta:
        model = SafetyMessage
        fields = ('created','modified','contents')

class CardSectionInline(OrderedTabularInline):
    model = CardSection
    fields = ('title', 'contents', 'is_gradable', 'check_count', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'title':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


@admin.register(Card)
class CardAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    form = CardForm
    inlines = (CardSectionInline, )
    list_display = ['title', 'tag_list']
    list_filter = [TaggitListFilter]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def get_urls(self):
        urls = super().get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('card_section', 'grade', 'checks_done')
    extra = 0


@admin.register(Observation)
class ObservationAdmin(ExportActionModelAdmin, admin.ModelAdmin):
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
    form = DeckForm
    list_display = ('title', 'description', 'boards_using_this_deck')
    readonly_fields = ('boards_using_this_deck', )
    filter_horizontal = ('cards', )

    def boards_using_this_deck(self, deck):
        return ", ".join([self.board_url(board) for board in deck.board_set.all()]) or "-"
    boards_using_this_deck.allow_tags = True

    def board_url(self, board):
        board_admin_url = reverse('admin:huddle_board_board_change', args=[board.id])
        return '<a href="{url}">{title}</a>'.format(url=board_admin_url, title=board.title)

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
class SafetyMessageAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('to_string', 'created', 'modified')

    def to_string(self, obj):
        return str(obj)
    to_string.short_description = 'Contents'



@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass


admin.site.unregister(Tag)


class ProxyTag(Tag):
    class Meta:
        proxy = True
        verbose_name = 'tag'


@admin.register(ProxyTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}

@admin.register(Answer)
class AnswerAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('__str__', 'card_section')
    resource_class = AnswerResource
