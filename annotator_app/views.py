from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from annotator_app.forms import AnnotateWorkoutForm, ConsentForm, UploadFileForm
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
            id_ts_map[request.POST['prolific_id']] = str(int(time.time()) * 1000)
            return HttpResponseRedirect('/annotator/upload_strava_workout/' + request.POST['prolific_id'])
    else:
        form = ConsentForm()
    return render(request, 'informed_consent.html', {'form': form})

def upload_strava_workout(request, prolific_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['screenshot_strava_workout'], prolific_id)
            return HttpResponseRedirect('/annotator/annotate_strava_workout/' + prolific_id)
    else:
        form = UploadFileForm()
    return render(request, 'upload_strava_workout.html', {'form': form})

def handle_uploaded_file(f, id):
    file_name = f'./data/{id}-{id_ts_map[id]}.png'
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # Send file to Bucket
    print('ready to upload to bucket with id ' + id + ' and ts ' + id_ts_map[id])
    bucket.upload_workout_screenshot(int(id_ts_map[id]), file_name)
    # Then we delete the local file
    os.remove(file_name)

def annotate_strava_workout(request, prolific_id):
    if request.method == 'POST':
        form = AnnotateWorkoutForm(request.POST)
        if form.is_valid():
            print(request.POST['pace'])
            print(request.POST['keywords'])
            print(request.POST['question1'])

            # Save annotation to bucket
            print('ready to annotate to bucket with id ' + prolific_id + ' and ts ' + id_ts_map[prolific_id])
            values = (prolific_id,)
            bucket.save_workout_annotation(values, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/')
    else:
        form = AnnotateWorkoutForm()

    return render(request, 'annotate_strava_workout.html', {'form': form, 'prolific_id': prolific_id})

def download_strava_workout(request, prolific_id):
    if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        print('ready to download to bucket with id ' + prolific_id + ' and ts ' + id_ts_map[prolific_id])
        file_content = bucket.download_workout_screenshot(int(id_ts_map[prolific_id]))
        return HttpResponse(file_content, content_type='image/png')