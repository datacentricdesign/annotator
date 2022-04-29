from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.http.response import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from non_data_provider.forms import ConsentForm, Annotate_sleep_data_Form, Disclosure_evaluation_Form
import time
from datetime import datetime
import os
from non_data_provider.models import Bucket
# from data_provider.models import Bucket

id_ts_map = {

}

BASE_URL = '/non_data_provider'


def index(request):
    """View function for home page of site."""
    context = {}
    if "PROLIFIC_ID" in request.GET:
        context["prolific_id"] = request.GET['PROLIFIC_ID']
        print(context)
    return render(request, 'index_non_data_provider.html', context=context)
    
@csrf_exempt
def informed_consent(request):
    prolific_id = None
    if "PROLIFIC_ID" in request.GET:
        prolific_id = request.GET['PROLIFIC_ID']
    if request.method == 'POST':
        form = ConsentForm(request.POST)
        if form.is_valid():
            ts = int(time.time()) * 1000
            id_ts_map[prolific_id] = ts
            Bucket.getInstance().save_prolific_id(prolific_id, ts)
            return HttpResponseRedirect('/annotate_sleep_data/' + prolific_id)
    else:
        form = ConsentForm()
    context = {
        "prolific_id": prolific_id,
        "form": form
    }
    return render(request, 'informed_consent_non_data_provider.html', context=context)



@csrf_exempt
def annotate_sleep_data(request, prolific_id):
    if request.method == 'POST':
        form = Annotate_sleep_data_Form(request.POST)
        if form.is_valid():
            
            q1 = request.POST['question1']
            q2 = request.POST['question2']
            q3 = request.POST['question3']
            q4 = request.POST['question4']
            q5 = request.POST['question5']

            # Save annotations to bucket
            values_questions = (q1, q2, q3, q4, q5)
            Bucket.getInstance().save_sleep_data_annotations(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/disclosure_evaluation/' + prolific_id)
    else:
        form = Annotate_sleep_data_Form()

    return render(request,'annotate_sleep_data.html', {'form': form, 'prolific_id': prolific_id})

# @csrf_exempt
# def download_strava_workout(request, prolific_id):
    # if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        # file_content = Bucket.getInstance().download_workout_screenshot(int(id_ts_map[prolific_id]))
        # return HttpResponse(file_content, content_type='image/png')


@csrf_exempt
def disclosure_evaluation(request, prolific_id):
    if request.method == 'POST':
        form = Disclosure_evaluation_Form(request.POST)
        if form.is_valid():
            q1 = request.POST['question1']
            q2 = request.POST['question2']
            q3 = request.POST['question3']
            q4 = request.POST['question4']
            q5 = request.POST['question5']
            # Save annotations to bucket
            values_questions = (q1, q2, q3, q4, q5)
            Bucket.getInstance().save_disclosure_evaluation_result(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/non_data_provider/thanks')
    else:
        form = Disclosure_evaluation_Form()

    return render(request,'disclosure_evaluation.html', {'form': form, 'prolific_id': prolific_id})

# @csrf_exempt
# def download_strava_overview(request, prolific_id):
    # if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        # file_content = Bucket.getInstance().download_overview_screenshot(int(id_ts_map[prolific_id]))
        # return HttpResponse(file_content, content_type='image/png')

@csrf_exempt
def thanks(request):
    context = {}
    return render(request, 'thanks.html', context=context)

@csrf_exempt
def leave(request):
    context = {}
    return render(request, 'leave.html', context=context)