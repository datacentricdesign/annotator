from django import forms

class ConsentForm(forms.Form):
    consent = forms.CheckboxInput()
    prolific_id = forms.TextInput()

class UploadWorkoutForm(forms.Form):
    screenshot_strava_workout = forms.FileField()

class UploadOverviewForm(forms.Form):
    screenshot_strava_overview = forms.FileField()

class AnnotateWorkoutForm(forms.Form):
    moving_time_min = forms.NumberInput()
    moving_time_sec = forms.NumberInput()
    distance = forms.NumberInput()
    pace = forms.NumberInput()
    time = forms.NumberInput()
    calories = forms.NumberInput()
    
    question1 = forms.Textarea()
    question2 = forms.Textarea()
    question3 = forms.Textarea()
    question4 = forms.Textarea()
    question5 = forms.Textarea()

class AnnotateOverviewForm(forms.Form):
    question1 = forms.Textarea()
    question2 = forms.Textarea()
    question3 = forms.Textarea()
    question4 = forms.Textarea()
    question5 = forms.Textarea()