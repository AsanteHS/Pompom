from django.conf.urls import url

from .views import HuddleBoardView, PlaceholderView

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^huddle_board/$', HuddleBoardView.as_view(), name="huddle_board"),
    url(r'^observe_card/$', PlaceholderView.as_view(), name="observe_card"),
]
