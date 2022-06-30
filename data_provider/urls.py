from django.urls import path
from . import views



urlpatterns = [
    # path('', views.index, name='index'),

    path('pre/informed_consent/', views.informed_consent_pre, name='informed_consent_pre'),
    path('pre/upload_sleep_data/<prolific_id>', views.upload_sleep_data, name='upload_sleep_data'),
    path('pre/thanks/', views.thanks_pre, name='thanks_pre'),

    path('main/informed_consent/', views.informed_consent_main, name='informed_consent_main'),
    path('main/annotate_sleep_data/<prolific_id>', views.annotate_sleep_data, name='annotate_sleep_data'),
    path('main/disclosure_evaluation/<prolific_id>', views.disclosure_evaluation, name='disclosure_evaluation'),
    path('main/download_sleep_data/<prolific_id>', views.download_sleep_data, name='download_sleep_data'),
    path('main/thanks/', views.thanks_main, name='thanks_main'),
   
]