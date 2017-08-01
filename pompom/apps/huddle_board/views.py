from django.views.generic import TemplateView


class HuddleBoardView(TemplateView):
    template_name = 'pompom/huddle_board.html'
