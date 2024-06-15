# chat/routing.py
from django.urls import path
from django.urls.conf import partial
from . import consumers


websocket_urlpatterns: list[partial] = [
    path("ws/general_game/<uuid:game_id>/", consumers.GeneralGameConsumer.as_asgi()),
    path("ws/login/", consumers.LoginConsumer.as_asgi()),
    path("ws/general_game/wait/", consumers.GeneralGameWaitConsumer.as_asgi()),
    path("ws/tournament_game/wait/", consumers.TournamentGameWaitConsumer.as_asgi()),
    path(
        "ws/tournament_game/<str:tournament_name>/",
        consumers.TournamentGameConsumer.as_asgi(),
    ),
    path(
        "ws/tournament_game/<str:tournament_name>/<int:round>/",
        consumers.TournamentGameRoundConsumer.as_asgi(),
    ),
]
