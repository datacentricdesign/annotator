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
from data_provider.models import STUDY_ID, Bucket

id_ts_map = {

}

BASE_URL = '/'


def index(request):
    """View function for home page of site."""
    context = {}
    if "PROLIFIC_ID" in request.GET:
        context["prolific_id"] = request.GET['PROLIFIC_ID']
        print(context)
    # Show template according to the type of participants
    print(STUDY_ID)
    if (STUDY_ID.endswith("NON_DATA_PROVIDER")):
        return render(request, 'index_non_data_provider.html', context=context)
    if (STUDY_ID.endswith("DATA_PROVIDER_TRACKER")):
        return render(request, 'index_non_data_provider_tracker.html', context=context)
    else:
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
            # Show template according to the type of participants
            if (STUDY_ID.endswith("NON_DATA_PROVIDER")):
                return HttpResponseRedirect('/annotate_sleep_data/' + prolific_id)
            if (STUDY_ID.endswith("NON_DATA_PROVIDER_TRACKER")):
                return HttpResponseRedirect('/annotate_sleep_data/' + prolific_id)
            else:
                return HttpResponseRedirect('/upload_sleep_data/' + prolific_id)

    else:
        form = ConsentForm()
    context = {
        "prolific_id": prolific_id,
        "form": form
    }
    # Show template according to the type of participants
    if (STUDY_ID.endswith("NON_DATA_PROVIDER")):
        return render(request, 'informed_consent_non_data_provider.html', context=context)
    if (STUDY_ID.endswith("NON_DATA_PROVIDER_TRACKER")):
        return render(request, 'informed_consent_non_data_provider_tracker.html', context=context)
            
    else:
        return render(request, 'informed_consent_data_provider.html', context=context)

@csrf_exempt
def upload_sleep_data(request, prolific_id):
    if request.method == 'POST':
        form = Upload_sleep_data_Form(request.POST, request.FILES)
        if form.is_valid():
            handle_sleep_file(request.FILES['screenshot_sleep_data'], prolific_id)
            return HttpResponseRedirect('/annotate_sleep_data/' + prolific_id)
    else:
        form = Upload_sleep_data_Form()
    return render(request,'upload_sleep_data.html', {'form': form})

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
        if (STUDY_ID.endswith("NON_DATA_PROVIDER") or STUDY_ID.endswith("NON_DATA_PROVIDER_TRACKER")):      
            # If participant is a non-data provider, download the previously uploaded picture
            timestamp = Bucket.getInstance().get_next_image_timestamp(prolific_id)
            Bucket.getInstance().save_ndp_timestamp(timestamp, int(id_ts_map[prolific_id]))    
        else:
            # If participant is a data provider, download the previously uploaded picture
            timestamp = int(id_ts_map[prolific_id])
            Bucket.getInstance().set_image_timestamp_dp(prolific_id, timestamp)
        # Download image from bucket
        file_content = Bucket.getInstance().download_sleep_screenshot(timestamp)
        return HttpResponse(file_content, content_type='image/png')

        

@csrf_exempt
def annotate_sleep_data(request, prolific_id):
    if request.method == 'POST':
        form = Annotate_sleep_data_Form(request.POST)
        if form.is_valid():
            q1 = "*"+request.POST['question1']+"*"
            q2 = request.POST['question2']+"*"
            q3 = request.POST['question3']+"*"
            q4 = request.POST['question4']+"*"
            q5 = request.POST['question5']+"*"
            

            # Save annotations to bucket, need to add instances
            values_questions = ("", "", "", "", "*", q5, q4, q3, q2, q1)
            Bucket.getInstance().save_sleep_data_annotation(values_questions, int(id_ts_map[prolific_id]))
            return HttpResponseRedirect('/disclosure_evaluation/' + prolific_id)
    else:
        form = Annotate_sleep_data_Form()

    # Change the introduction sentence according to STUDY_ID
    intro_sentence = ''
    example_sentence = ''

    if (STUDY_ID.endswith("DATA_PROVIDER")):
        intro_sentence +=  'The screenshot on the left captures your sleep data of the past week as uploaded in the previous step.'
        example_sentence += 'Example: Achieving sleep goals was difficult for me, because I am more productive in the evening and I usually work before sleeping. When I am so engrossed in work, it is hard to immediately stop working and go to bed. Recenlty, I am trying to get up and sleep early, which seems going well!'
    else:
        intro_sentence += 'The screenshot on the left captures the Apple Sleep data of someone in your age range.'
        example_sentence += 'Example: Achieving sleep goals has been very difficult for me, even for the average sleep time in bed. I am more productive in the evening, so I work after dinner quite often. When I am so engrossed in work, it is hard to immediately stop working and go to bed, even when it is bedtime.'
    
    return render(request, 'annotate_sleep_data.html', {'form': form, 'prolific_id': prolific_id, 'intro_sentence': intro_sentence,'example_sentence':example_sentence})  

        
@csrf_exempt
def disclosure_evaluation(request, prolific_id):
    if request.method == 'POST':
        form = Disclosure_evaluation_Form(request.POST)
        # need to change it to questions
        if form.is_valid():
            trust = int(request.POST['trust_level'])
            intimacy = int(request.POST['intimacy_level'])
            entertainment = int(request.POST['entertainment_level'])
            
            # Save evaluation result to bucket
            trust_values = (trust,)
            Bucket.getInstance().save_trust_level(trust_values, int(id_ts_map[prolific_id]))
            Bucket.getInstance().save_intimacy_level((intimacy,), int(id_ts_map[prolific_id]))
            Bucket.getInstance().save_entertainment_level((entertainment,), int(id_ts_map[prolific_id]))

            # 
            Bucket.getInstance().image_timestamp_done(prolific_id)
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

