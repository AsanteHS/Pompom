from django.views.generic import TemplateView


class HuddleBoardView(TemplateView):
    template_name = 'huddle_board/huddle_board.html'


class PerformObservationView(TemplateView):
    template_name = 'huddle_board/observation.html'
