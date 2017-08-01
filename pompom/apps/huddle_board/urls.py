from django.conf.urls import url

from .views import HuddleBoardView

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^huddle_board/$', HuddleBoardView.as_view(), name="huddle_board"),
]
