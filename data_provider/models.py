# Create your models here.
from django.db import models
from dcd.bucket.thing import Thing

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
        # need to add a new property in bucket, name it sleep_data_property
        self.sleep_data_property = self.thing.find_or_create_property(
                "Sleep data Screenshot", "IMAGE_PNG")

        self.prolific_id_property = self.thing.find_or_create_property(
                "Prolific ID", "TEXT")

        self.sleep_data_annotation_property = self.thing.find_or_create_property(
                "Sleep Data Annotations", "STRAVA_ANNOTATIONS")

        self.disclosure_evaluation_property = self.thing.find_or_create_property(
                 "Disclosure Evaluation Result", "STRAVA_ANNOTATIONS")

        
    def upload_sleep_screenshot(self, ts, file_name):
        values = (100,100)
        self.sleep_data_property.update_values(values, ts, file_name=file_name)

    def download_sleep_screenshot(self, ts):
        return self.sleep_data_property.read_media('image-png', ts)

    def save_sleep_data_annotation(self, values, ts):
        self.sleep_data_annotation_property.update_values(values=values, time_ms=ts)

    def save_prolific_id(self, prolific_id, ts):
        values = (prolific_id,)
        self.prolific_id_property.update_values(values=values, time_ms=ts)

    def save_disclosure_evaluation_result(self, values, ts):
         self.disclosure_evaluation_property.update_values(values=values, time_ms=ts)
    

    # def upload_overview_screenshot(self, ts, file_name):
        # values = (100,100)
        # self.overview_screenshot_property.update_values(values, ts, file_name=file_name)

    # def download_overview_screenshot(self, ts):
       # return self.overview_screenshot_property.read_media('image-png', ts)

    # def save_workout_annotation_metrics(self, values, ts):
        # self.workout_annotation_metrics_property.update_values(values=values, time_ms=ts)
    
    