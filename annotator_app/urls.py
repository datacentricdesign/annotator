from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('informed_consent/', views.informed_consent, name='informed_consent'),
    path('upload_strava_workout/<prolific_id>', views.upload_strava_workout, name='upload_strava_workout'),
    path('download_strava_workout/<prolific_id>', views.download_strava_workout, name='download_strava_workout'),
    path('annotate_strava_workout/<prolific_id>', views.annotate_strava_workout, name='annotate_strava_workout'),
]