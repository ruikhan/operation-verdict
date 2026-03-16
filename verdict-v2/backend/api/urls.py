from django.urls import path
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('health/', health_check),

    path('auth/register/',       views.RegisterView.as_view()),
    path('auth/token/',          TokenObtainPairView.as_view()),
    path('auth/token/refresh/',  TokenRefreshView.as_view()),

    path('player/profile/',            views.ProfileView.as_view()),
    path('player/accept-terms/',       views.AcceptTermsView.as_view()),
    path('player/cinematic-complete/', views.CinematicCompleteView.as_view()),

    path('files/',                      views.VictimFileListView.as_view()),
    path('files/<str:file_id>/',        views.VictimFileDetailView.as_view()),
    path('files/<str:file_id>/review/', views.ReviewFileView.as_view()),
    path('files/<str:file_id>/cipher/', views.SolveCipherView.as_view()),

    path('timer/update/',         views.UpdateTimerView.as_view()),
    path('progress/',             views.GameProgressView.as_view()),
    path('leaderboard/',          views.LeaderboardView.as_view()),

    path('interrogation/start/',              views.StartInterrogationView.as_view()),
    path('interrogation/<int:session_id>/message/', views.SendInterrogationMessageView.as_view()),

    path('tips/',               views.TipListView.as_view()),
    path('tips/<int:tip_id>/read/', views.ReadTipView.as_view()),

    path('corruption/',                       views.CorruptionEventListView.as_view()),
    path('corruption/<int:event_id>/resolve/',views.ResolveCorruptionView.as_view()),

    path('timeline/', views.TimelineView.as_view()),
]