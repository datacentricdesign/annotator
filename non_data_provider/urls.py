from django.urls import path
from . import views

BASE_URL = '/non_data_provider'

urlpatterns = [
    path('', views.index, name='index'),
    path('informed_consent/', views.informed_consent, name='informed_consent'),
    
    # path('download_strava_workout/<prolific_id>', views.download_strava_workout, name='download_strava_workout'),
    path('annotate_sleep_data/<prolific_id>', views.annotate_sleep_data, name='annotate_sleep_data'),
    
    # path('download_strava_overview/<prolific_id>', views.download_strava_overview, name='download_strava_overview'),
    path('disclosure_evaluation/<prolific_id>', views.disclosure_evaluation, name='disclosure_evaluation'),
    path('thanks/', views.thanks, name='thanks'),
    path('leave/', views.leave, name='leave'),
]