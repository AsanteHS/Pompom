from django.conf.urls import url

from .views import HuddleBoardView, PerformObservationView, SuccessView, HomeView, MobileMenuView

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^huddle_board/$', HuddleBoardView.as_view(), name="huddle_board"),
    url(r'^mobile_menu/(?P<pk>\d+)/$', MobileMenuView.as_view(), name="mobile_menu"),
    url(r'^perform_observation/$', PerformObservationView.as_view(), name="perform_observation"),
    url(r'^success/$', SuccessView.as_view(), name="success"),
]
