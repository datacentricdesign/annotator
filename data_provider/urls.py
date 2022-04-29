from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('informed_consent/', views.informed_consent, name='informed_consent'),
    path('upload_sleep_data/<prolific_id>', views.upload_sleep_data, name='upload_sleep_data'),
    path('annotate_sleep_data/<prolific_id>', views.annotate_sleep_data, name='annotate_sleep_data'),
    path('disclosure_evaluation/<prolific_id>', views.disclosure_evaluation, name='disclosure_evaluation'),
    path('thanks/', views.thanks, name='thanks'),
    path('leave/', views.leave, name='leave'),
    # path('upload_strava_overview/<prolific_id>', views.upload_strava_overview, name='upload_strava_overview'),
    # path('download_strava_overview/<prolific_id>', views.download_strava_overview, name='download_strava_overview'),
    path('download_sleep_data/<prolific_id>', views.download_sleep_data, name='download_sleep_data'),
   
]