from django.conf.urls import url

from .views import HuddleBoardView, PerformObservationView, HomeView, MobileMenuView, AddCardNoteView

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^huddle_board/(?P<pk>\d+)/$', HuddleBoardView.as_view(), name="huddle_board"),
    url(r'^mobile_menu/(?P<pk>\d+)/$', MobileMenuView.as_view(), name="mobile_menu"),
    url(r'^perform_observation/(?P<pk>\d+)/$', PerformObservationView.as_view(), name="perform_observation"),
    url(r'^card_note/(?P<pk>\d+)/$', AddCardNoteView.as_view(), name="add_card_note"),
]
