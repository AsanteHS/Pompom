from django.conf.urls import url

from .views import HuddleBoardView, PerformObservationView

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^huddle_board/$', HuddleBoardView.as_view(), name="huddle_board"),
    url(r'^perform_observation/$', PerformObservationView.as_view(), name="perform_observation"),
]
