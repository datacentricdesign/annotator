# Create your models here.
from multiprocessing.dummy import Array
from django.db import models
from dcd.bucket.thing import Thing
import environ

env = environ.Env()
environ.Env.read_env(env_file=".env")
STUDY_ID = env("STUDY_ID")

TO_ANNOTATE_FILE = "to_annotate.txt"
DONE_FILE = "done.txt"

class Bucket:

    __instance = None
    @staticmethod
    def getInstance():
      """ Static access method. """
      if Bucket.__instance == None:
         Bucket.__instance = Bucket()
      return Bucket.__instance

    def __init__(self):
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
        
        self.timestamps_to_annotate = self.load_timestamps_to_annotate()

    def save_prolific_id(self, prolific_id, ts):
        values = (prolific_id,)
        self.prolific_id_property.update_values(values=values, time_ms=ts)

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


    def save_trust_level(self, trust_level, ts):
        values = (trust_level,)
        self.trust_level_property.update_values(values=values, time_ms=ts)

    def save_intimacy_level(self, intimacy_level, ts):
        values = (intimacy_level,)
        self.intimacy_level_property.update_values(values=values, time_ms=ts)

    def save_entertainment_level(self, entertainment_level, ts):
        values = (entertainment_level,)
        self.entertainment_level_property.update_values(values=values, time_ms=ts)

    def load_timestamps(self, file_name):
        with open(file_name, 'r') as file:
            # read the file, split into lines (timestamps) and convert into int
            return [int(i) for i in file.read().splitlines()]

    def load_timestamps_to_annotate(self) -> Array[int]:
        to_annotate = self.load_timestamps(TO_ANNOTATE_FILE)
        done = self.load_timestamps(DONE_FILE)
        # remove all elements from done in to_annotate
        return filter(lambda i: i not in done, to_annotate)

    def get_next_image_timestamp(self):
        timestamp = self.timestamps_to_annotate.pop(0)
        with open(DONE_FILE, 'a') as file:
            file.write("\n" + str(timestamp))
        return timestamp
