from django import forms

class ConsentForm(forms.Form):
    consent = forms.CheckboxInput()
    prolific_id = forms.TextInput()

class Upload_sleep_data_Form(forms.Form):
    screenshot_sleep_data = forms.FileField()

class Annotate_sleep_data_Form(forms.Form):
   
    question1 = forms.Textarea()
    question2 = forms.Textarea()
    question3 = forms.Textarea()
    question4 = forms.Textarea()
    question5 = forms.Textarea()

class Disclosure_evaluation_Form(forms.Form):
    question1 = forms.Textarea()
    question2 = forms.Textarea()
    question3 = forms.Textarea()
    question4 = forms.Textarea()
    question5 = forms.Textarea()