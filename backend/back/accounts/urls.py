from django.urls import path
from django.urls.conf import partial
from . import views
from .views import logout_view

urlpatterns: list[partial] = [
    path("me/", views.MeViewSet.as_view({"get": "list"}), name="me"),
    path(
        "users/",
        views.UsersViewSet.as_view({"get": "list"}),
        name="users",
    ),
    path(
        "users/<str:intra_id>/",
        views.UsersDetailViewSet.as_view({"get": "list", "patch": "partial_update"}),
        name="users_detail",
    ),
    path("login/", views.Login42APIView.as_view()),
    path("login/42/callback/", views.CallbackAPIView.as_view()),
    path("logout/", logout_view, name="logout"),
    path(
        "login/<str:intra_id>/",
        views.TestAccountLogin.as_view(),
        name="test_user_login",
    ),
    path("chart/", views.ChartViewSet.as_view({"get": "list"}), name="chart"),
]
