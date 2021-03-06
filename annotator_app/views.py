from django.http.response import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from annotator_app.forms import AnnotateWorkoutForm, AnnotateOverviewForm, ConsentForm, UploadWorkoutForm, UploadOverviewForm
import time
from datetime import datetime
import os


from annotator_app.models import Bucket

id_ts_map = {

}

def index(request):
    """View function for home page of site."""
    context = {}
    if "PROLIFIC_ID" in request.GET:
        context["prolific_id"] = request.GET['PROLIFIC_ID']   
    return render(request, 'index.html', context=context)
    
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
            return HttpResponseRedirect('/annotator/upload_strava_workout/' + prolific_id)
    else:
        form = ConsentForm()
    context = {
        "prolific_id": prolific_id,
        "form": form
    }
    return render(request, 'informed_consent.html', context=context)

@csrf_exempt
def upload_strava_workout(request, prolific_id):
    if request.method == 'POST':
        form = UploadWorkoutForm(request.POST, request.FILES)
        if form.is_valid():
            handle_workout_file(request.FILES['screenshot_strava_workout'], prolific_id)
            return HttpResponseRedirect('/annotator/annotate_strava_workout/' + prolific_id)
    else:
        form = UploadWorkoutForm()
    return render(request, 'upload_strava_workout.html', {'form': form})

@csrf_exempt
def handle_workout_file(f, id):
    file_name = f'./data/{id}-{id_ts_map[id]}-workout.png'
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # Send file to Bucket
    Bucket.getInstance().upload_workout_screenshot(int(id_ts_map[id]), file_name)
    # Then we delete the local file
    os.remove(file_name)

@csrf_exempt
def annotate_strava_workout(request, prolific_id):
    if request.method == 'POST':
        form = AnnotateWorkoutForm(request.POST)
        if form.is_valid():
            calories = 0
            moving_time = int(request.POST['moving_time_minute'])*60 + int(request.POST['moving_time_second'])
            distance = float(request.POST['distance'])
            pace = int(request.POST['pace_minute'])*60 + int(request.POST['pace_second'])
            
            datestr=request.POST['date']
            time_hour=int(request.POST['run_time_hour'])
            time_minute=int(request.POST['run_time_minute'])
            timestr= datestr +'-'+ str(time_hour)+'-'+str(time_minute)
            t = datetime.strptime(timestr,'%Y-%m-%d-%H-%M')
            time1 = time.mktime(t.timetuple())
            

            # Save annotation metrics to bucket
            values_metrics = (moving_time, distance, pace, time1, calories)
            Bucket.getInstance().save_workout_annotation_metrics(values_metrics, int(id_ts_map[prolific_id]))

            q1 = request.POST['question1']
            q2 = request.POST['question2']
            q3 = request.POST['question3']
            q4 = request.POST['question4']
            q5 = request.POST['question5']
            # Save annotations to bucket
            values_questions = (q1, q2, q3, q4, q5)
            Bucket.getInstance().save_workout_annotations(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/annotator/upload_strava_overview/' + prolific_id)
    else:
        form = AnnotateWorkoutForm()

    return render(request, 'annotate_strava_workout.html', {'form': form, 'prolific_id': prolific_id})

@csrf_exempt
def download_strava_workout(request, prolific_id):
    if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        file_content = Bucket.getInstance().download_workout_screenshot(int(id_ts_map[prolific_id]))
        return HttpResponse(file_content, content_type='image/png')

@csrf_exempt
def upload_strava_overview(request, prolific_id):
    if request.method == 'POST':
        form = UploadOverviewForm(request.POST, request.FILES)
        if form.is_valid():
            handle_overview_file(request.FILES['screenshot_strava_overview'], prolific_id)
            return HttpResponseRedirect('/annotator/annotate_strava_overview/' + prolific_id)
    else:
        form = UploadOverviewForm()
    return render(request, 'upload_strava_overview.html', {'form': form})

@csrf_exempt
def handle_overview_file(f, id):
    file_name = f'./data/{id}-{id_ts_map[id]}-overview.png'
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # Send file to Bucket
    Bucket.getInstance().upload_overview_screenshot(int(id_ts_map[id]), file_name)
    # Then we delete the local file
    os.remove(file_name)

@csrf_exempt
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
            Bucket.getInstance().save_overview_annotations(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/annotator/thanks')
    else:
        form = AnnotateOverviewForm()

    return render(request, 'annotate_strava_overview.html', {'form': form, 'prolific_id': prolific_id})

@csrf_exempt
def download_strava_overview(request, prolific_id):
    if (id_ts_map[prolific_id] is not None):
        # Download image from bucket
        file_content = Bucket.getInstance().download_overview_screenshot(int(id_ts_map[prolific_id]))
        return HttpResponse(file_content, content_type='image/png')

@csrf_exempt
def thanks(request):
    context = {}
    return render(request, 'thanks.html', context=context)

@csrf_exempt
def leave(request):
    context = {}
    return render(request, 'leave.html', context=context)