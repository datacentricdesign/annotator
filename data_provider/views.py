# Create your views here.
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from data_provider.forms import ConsentForm, Upload_sleep_data_Form, Annotate_sleep_data_Form, Disclosure_evaluation_Form
import time
from datetime import datetime
import os
from data_provider.models import Bucket

id_ts_map = {

}

BASE_URL = '/'


def index(request):
    """View function for home page of site."""
    context = {}
    if "PROLIFIC_ID" in request.GET:
        context["prolific_id"] = request.GET['PROLIFIC_ID']
        print(context)
    return render(request, 'index_data_provider.html', context=context)
  
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
            Bucket.getInstance().save_study_id(ts)
            return HttpResponseRedirect('/upload_sleep_data/' + prolific_id)
    else:
        form = ConsentForm()
    context = {
        "prolific_id": prolific_id,
        "form": form
    }
    return render(request, 'informed_consent_data_provider.html', context=context)

@csrf_exempt
def upload_sleep_data(request, prolific_id):
    if request.method == 'POST':
        form = Upload_sleep_data_Form(request.POST, request.FILES)
        if form.is_valid():
            handle_sleep_file(request.FILES['screenshot_sleep_data'], prolific_id)
            print("handled file")
            return HttpResponseRedirect('/annotate_sleep_data/' + prolific_id)
    else:
        form = Upload_sleep_data_Form()
    return render(request,'upload_sleep_data.html', {'form': form})

@csrf_exempt
def handle_sleep_file(f, id):
    file_name = f'./data/{id_ts_map[id]}.png'
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # Send file to Bucket
    Bucket.getInstance().upload_sleep_screenshot(int(id_ts_map[id]), file_name)
    # Then we delete the local file
    os.remove(file_name)


@csrf_exempt
def download_sleep_data(request, prolific_id):
    if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        file_content = Bucket.getInstance().download_sleep_screenshot(int(id_ts_map[prolific_id]))
        return HttpResponse(file_content, content_type='image/png')

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

            # Save annotations to bucket, need to add instances
            values_questions = (q1, q2, q3, q4, q5, "", "", "", "", "")
            Bucket.getInstance().save_sleep_data_annotation(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/disclosure_evaluation/' + prolific_id)
    else:
        form = Annotate_sleep_data_Form()

    return render(request, 'annotate_sleep_data_data_provider.html', {'form': form, 'prolific_id': prolific_id})

@csrf_exempt
def disclosure_evaluation(request, prolific_id):
    if request.method == 'POST':
        form = Disclosure_evaluation_Form(request.POST)
        # need to change it to questions
        if form.is_valid():
            trust = request.POST['trust_level']
            intimacy = request.POST['intimacy_level']
            entertainment = request.POST['entertainment_level']

            # Save evaluation result to bucket
            Bucket.getInstance().save_trust_level((trust,), int(id_ts_map[prolific_id]))
            Bucket.getInstance().save_intimacy_level((intimacy,), int(id_ts_map[prolific_id]))
            Bucket.getInstance().save_entertainment_level((entertainment,), int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/thanks')
    else:
        form = Disclosure_evaluation_Form()

    return render(request,'disclosure_evaluation.html', {'form': form, 'prolific_id': prolific_id})


@csrf_exempt
def thanks(request):
    context = {}
    return render(request, 'thanks.html', context=context)

@csrf_exempt
def leave(request):
    context = {}
    return render(request, 'leave.html', context=context)



# @csrf_exempt
# def upload_strava_overview(request, prolific_id):
    # if request.method == 'POST':
       # form = UploadOverviewForm(request.POST, request.FILES)
      #  if form.is_valid():
           # handle_overview_file(request.FILES['screenshot_strava_overview'], prolific_id)
           # return HttpResponseRedirect('/annotate_strava_overview/' + prolific_id)
    # else:
        #form = UploadOverviewForm()
    # return render(request,'upload_strava_overview.html', {'form': form})

# @csrf_exempt
# def handle_overview_file(f, id):
   # file_name = f'./data/{id}-{id_ts_map[id]}-overview.png'
   # with open(file_name, 'wb+') as destination:
       # for chunk in f.chunks():
            # destination.write(chunk)
    # Send file to Bucket
    # Bucket.getInstance().upload_overview_screenshot(int(id_ts_map[id]), file_name)
    # Then we delete the local file
    # os.remove(file_name)


# @csrf_exempt
# def download_strava_overview(request, prolific_id):
   # if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        # file_content = Bucket.getInstance().download_overview_screenshot(int(id_ts_map[prolific_id]))
        # return HttpResponse(file_content, content_type='image/png')

