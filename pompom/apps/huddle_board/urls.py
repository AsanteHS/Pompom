from django.conf.urls import url
from django.views.defaults import server_error

from .views import HuddleBoardView, PerformObservationView, HomeView, MobileMenuView, AddCardNoteView, ChooseCardView, \
    EnterPasswordView, HuddleBoardCardsView, HuddleBoardHistoryView, HuddleBoardSafetyView, HuddleBoardQRView

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^huddle_board/(?P<pk>\d+)/$', HuddleBoardView.as_view(), name="huddle_board"),
    url(r'^huddle_board/(?P<pk>\d+)/cards/$', HuddleBoardCardsView.as_view(), name="huddle_board_cards"),
    url(r'^huddle_board/(?P<pk>\d+)/history/$', HuddleBoardHistoryView.as_view(), name="huddle_board_history"),
    url(r'^huddle_board/(?P<pk>\d+)/safety/$', HuddleBoardSafetyView.as_view(), name="huddle_board_safety"),
    url(r'^huddle_board/(?P<pk>\d+)/qr/$', HuddleBoardQRView.as_view(), name="huddle_board_qr"),

    url(r'^mobile_menu/(?P<pk>\d+)/(?P<token>[^/]+)/$', MobileMenuView.as_view(), name="mobile_menu"),
    url(r'^choose_card/(?P<pk>\d+)/(?P<token>[^/]+)/$', ChooseCardView.as_view(), name="choose_card"),
    url(r'^perform_observation/(?P<pk>\d+)/(?P<token>[^/]+)/$', PerformObservationView.as_view(),
        name="perform_observation"),
    url(r'^card_note/(?P<pk>\d+)/(?P<token>[^/]+)/$', AddCardNoteView.as_view(), name="add_card_note"),

    url(r'^enter_password/$', EnterPasswordView.as_view(), name="enter_password"),
    url(r'^500/$', server_error, name="500"),
]
