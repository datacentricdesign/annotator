# Create your models here.
from multiprocessing.dummy import Array
from django.db import models
from dcd.bucket.thing import Thing
import environ
import threading
import time

import requests

env = environ.Env()
environ.Env.read_env(env_file=".env")
STUDY_ID = env("STUDY_ID")
PROLIFIC_API = env("PROLIFIC_API")
PROLIFIC_STUDY_ID = env("PROLIFIC_STUDY_ID")

TO_ANNOTATE_FILE = "data/to_annotate_" + STUDY_ID + ".txt"
DONE_FILE = "data/done_" + STUDY_ID + ".txt"


class ProlificReturn(threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
      while(True):
          time.sleep(5)
          Bucket.getInstance().check_prolific_submissions()

class Bucket:

    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if Bucket.__instance == None:
            Bucket.__instance = Bucket()
        return Bucket.__instance

    def __init__(self):
        print('init Bucket model')
        self.thing = Thing()

        self.prolific_id_property = self.thing.find_or_create_property(
                "Prolific ID", "TEXT")

        self.study_id_property = self.thing.find_or_create_property(
                "Study ID", "TEXT")

        self.sleep_data_property = self.thing.find_or_create_property(
                "Sleep data Screenshot", "IMAGE_PNG")

        self.sleep_data_annotation_property = self.thing.find_or_create_property(
                "Sleep Data Annotations", "SURVEY_10_OPEN_QUESTIONS")

        self.trust_level_property = self.thing.find_or_create_property(
                 "Trust Level", "TRUST_LEVEL")

        self.intimacy_level_property = self.thing.find_or_create_property(
                 "Intimacy Level", "INTIMACY_LEVEL")

        self.entertainment_level_property = self.thing.find_or_create_property(
                "Entertainment Level", "ENTERTAINMENT_LEVEL")

        self.ndp_timestamp_property = self.thing.find_or_create_property(
                 "NDP Timestamp", "STATE")
        
        self.timestamps_to_annotate = self.load_timestamps_to_annotate()

        self.ongoing = {}
        self.prolific_status = {}
        self.thread_prolific_return = ProlificReturn(1, "Prolific Return", 1)
        self.thread_prolific_return.start()

    def check_prolific_submissions(self):
        print('check prolific return')
        uri = f'https://api.prolific.co/api/v1/studies/{PROLIFIC_STUDY_ID}/submissions/'
        result = requests.get(uri, headers={'Authorization': f'Token {PROLIFIC_API}'})
        json_results = result.json()
        for submission in json_results['results']:
            participant_id = submission['participant_id']
            status = submission['status']
            if status == 'RETURNED' and self.ongoing.get(participant_id) is not None:
                # we need to save the unused image timestamp
                timestamp = self.ongoing.pop(participant_id)
                self.timestamps_to_annotate.append(timestamp)

    def save_prolific_id(self, prolific_id, ts):
        values = (prolific_id,)
        self.prolific_id_property.update_values(values=values, time_ms=ts)

    def save_ndp_timestamp(self, ndp_timestamp, ts):
        values = (ndp_timestamp,)
        self.ndp_timestamp_property.update_values(values=values, time_ms=ts)

    def save_study_id(self, ts):
        values = (STUDY_ID,)
        self.study_id_property.update_values(values=values, time_ms=ts)
        
    def upload_sleep_screenshot(self, ts, file_name):
        values = (100,100)
        self.sleep_data_property.update_values(values, ts, file_name=file_name)

    def download_sleep_screenshot(self, ts):
        return self.sleep_data_property.read_media('image-png', ts)

    def save_sleep_data_annotation(self, values, ts):
        self.sleep_data_annotation_property.update_values(values=values, time_ms=ts)


    def save_trust_level(self, values, ts):
        self.trust_level_property.update_values(values=values, time_ms=ts)
        
    def save_intimacy_level(self, values, ts):
        print(values)
        self.intimacy_level_property.update_values(values=values, time_ms=ts)

    def save_entertainment_level(self, values, ts):
        self.entertainment_level_property.update_values(values=values, time_ms=ts)

    def load_timestamps(self, file_name):
        with open(file_name, 'r') as file:
            # read the file, split into lines (timestamps) and convert into int
            ts_array = []
            for line in file.read().splitlines():
                try:
                    ts_array.append(int(line))
                except:
                    print("not a timestamp!")
            return ts_array

    def load_timestamps_to_annotate(self):
        to_annotate = self.load_timestamps(TO_ANNOTATE_FILE)
        done = self.load_timestamps(DONE_FILE)
        # remove all elements from done in to_annotate
        return list(filter(lambda i: i not in done, to_annotate))

    def get_next_image_timestamp(self, prolific_id):
        timestamp = self.timestamps_to_annotate.pop(0)
        self.ongoing[prolific_id] = timestamp
        return timestamp

    def image_timestamp_done(self, prolific_id):
        timestamp = self.ongoing.pop(prolific_id)
        with open(DONE_FILE, 'a') as file:
            file.write("\n" + str(timestamp))