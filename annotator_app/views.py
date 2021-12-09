from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from annotator_app.forms import AnnotateWorkoutForm, ConsentForm, UploadFileForm
import time

id_ts_map = {

}

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
    with open('test.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # TODO upload to bucket
    print('ready to upload to bucket with id ' + id + ' and ts ' + id_ts_map[id])

def annotate_strava_workout(request, prolific_id):
    if request.method == 'POST':
        form = AnnotateWorkoutForm(request.POST)
        if form.is_valid():
            print(request.POST['pace'])
            print(request.POST['keywords'])
            print(request.POST['question1'])

            # TODO save to bucket
            print('ready to annotate to bucket with id ' + prolific_id + ' and ts ' + id_ts_map[prolific_id])
            return HttpResponseRedirect('/')
    else:
        form = AnnotateWorkoutForm()

    return render(request, 'annotate_strava_workout.html', {'form': form})

def download_strava_workout_screenshot(request, prolific_id):
    if (id_ts_map[prolific_id] is not None):
        # TODO download image from bucket
        print('ready to download to bucket with id ' + prolific_id + ' and ts ' + id_ts_map[prolific_id])
        return 