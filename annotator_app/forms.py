from django import forms

class ConsentForm(forms.Form):
    consent = forms.CheckboxInput()
    prolific_id = forms.TextInput()

class UploadFileForm(forms.Form):
    screenshot_strava_workout = forms.FileField()

class AnnotateWorkoutForm(forms.Form):
    pace = forms.NumberInput()
    keywords = forms.TextInput()
    question1 = forms.Textarea()