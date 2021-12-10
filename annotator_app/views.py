from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from annotator_app.forms import AnnotateWorkoutForm, AnnotateOverviewForm, ConsentForm, UploadWorkoutForm, UploadOverviewForm
import time
import os

from annotator_app.models import Bucket

id_ts_map = {

}

bucket = Bucket()

def index(request):
    """View function for home page of site."""

    context = {}
    return render(request, 'index.html', context=context)

def informed_consent(request):
    if request.method == 'POST':
        form = ConsentForm(request.POST)
        if form.is_valid():
            prolific_id = request.POST['prolific_id']
            ts = str(int(time.time()) * 1000)
            id_ts_map[prolific_id] = ts
            bucket.save_prolific_id(prolific_id, ts)
            return HttpResponseRedirect('/annotator/upload_strava_workout/' + request.POST['prolific_id'])
    else:
        form = ConsentForm()
    return render(request, 'informed_consent.html', {'form': form})

def upload_strava_workout(request, prolific_id):
    if request.method == 'POST':
        form = UploadWorkoutForm(request.POST, request.FILES)
        if form.is_valid():
            handle_workout_file(request.FILES['screenshot_strava_workout'], prolific_id)
            return HttpResponseRedirect('/annotator/annotate_strava_workout/' + prolific_id)
    else:
        form = UploadWorkoutForm()
    return render(request, 'upload_strava_workout.html', {'form': form})

def handle_workout_file(f, id):
    file_name = f'./data/{id}-{id_ts_map[id]}-workout.png'
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # Send file to Bucket
    bucket.upload_workout_screenshot(int(id_ts_map[id]), file_name)
    # Then we delete the local file
    os.remove(file_name)

def annotate_strava_workout(request, prolific_id):
    if request.method == 'POST':
        form = AnnotateWorkoutForm(request.POST)
        if form.is_valid():
            moving_time = request.POST['moving_time']
            distance = request.POST['distance']
            pace = request.POST['pace']
            time = request.POST['time']
            calories = request.POST['calories']
            # Save annotation metrics to bucket
            values_metrics = (moving_time, distance, pace, time, calories)
            bucket.save_workout_annotation_metrics(values_metrics, int(id_ts_map[prolific_id]))

            q1 = request.POST['question1']
            q2 = request.POST['question2']
            q3 = request.POST['question3']
            q4 = request.POST['question4']
            q5 = request.POST['question5']
            # Save annotations to bucket
            values_questions = (q1, q2, q3, q4, q5)
            bucket.save_workout_annotations(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/annotator/upload_strava_overview/' + prolific_id)
    else:
        form = AnnotateWorkoutForm()

    return render(request, 'annotate_strava_workout.html', {'form': form, 'prolific_id': prolific_id})

def download_strava_workout(request, prolific_id):
    if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        file_content = bucket.download_workout_screenshot(int(id_ts_map[prolific_id]))
        return HttpResponse(file_content, content_type='image/png')

def upload_strava_overview(request, prolific_id):
    if request.method == 'POST':
        form = UploadOverviewForm(request.POST, request.FILES)
        if form.is_valid():
            handle_overview_file(request.FILES['screenshot_strava_overview'], prolific_id)
            return HttpResponseRedirect('/annotator/annotate_strava_overview/' + prolific_id)
    else:
        form = UploadOverviewForm()
    return render(request, 'upload_strava_overview.html', {'form': form})

def handle_overview_file(f, id):
    file_name = f'./data/{id}-{id_ts_map[id]}-overview.png'
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # Send file to Bucket
    bucket.upload_overview_screenshot(int(id_ts_map[id]), file_name)
    # Then we delete the local file
    os.remove(file_name)

def annotate_strava_overview(request, prolific_id):
    if request.method == 'POST':
        form = AnnotateOverviewForm(request.POST)
        if form.is_valid():
            q1 = request.POST['question1']
            q2 = request.POST['question2']
            q3 = request.POST['question3']
            q4 = request.POST['question4']
            q5 = request.POST['question5']
            # Save annotations to bucket
            values_questions = (q1, q2, q3, q4, q5)
            bucket.save_overview_annotations(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/annotator/thanks')
    else:
        form = AnnotateOverviewForm()

    return render(request, 'annotate_strava_overview.html', {'form': form, 'prolific_id': prolific_id})

def download_strava_overview(request, prolific_id):
    if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        file_content = bucket.download_overview_screenshot(int(id_ts_map[prolific_id]))
        return HttpResponse(file_content, content_type='image/png')

def thanks(request):
    context = {}
    return render(request, 'thanks.html', context=context)