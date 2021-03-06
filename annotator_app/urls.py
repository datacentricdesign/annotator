from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('informed_consent/', views.informed_consent, name='informed_consent'),
    path('upload_strava_workout/<prolific_id>', views.upload_strava_workout, name='upload_strava_workout'),
    path('download_strava_workout/<prolific_id>', views.download_strava_workout, name='download_strava_workout'),
    path('annotate_strava_workout/<prolific_id>', views.annotate_strava_workout, name='annotate_strava_workout'),
    path('upload_strava_overview/<prolific_id>', views.upload_strava_overview, name='upload_strava_overview'),
    path('download_strava_overview/<prolific_id>', views.download_strava_overview, name='download_strava_overview'),
    path('annotate_strava_overview/<prolific_id>', views.annotate_strava_overview, name='annotate_strava_overview'),
    path('thanks/', views.thanks, name='thanks'),
    path('leave/', views.leave, name='leave'),
]