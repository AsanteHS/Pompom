from django.views.generic import TemplateView

from pompom.apps.huddle_board.models import Card


class HuddleBoardView(TemplateView):
    template_name = 'huddle_board/huddle_board.html'


class PerformObservationView(TemplateView):
    template_name = 'huddle_board/observation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card'] = Card.objects.first()
        return context
