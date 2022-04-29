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

        # self.workout_screenshot_property = self.thing.find_or_create_property(
                # "Strava Workout Screenshot", "IMAGE_PNG")

        self.prolific_id_property = self.thing.find_or_create_property(
                "Prolific ID", "TEXT")

        self.sleep_data_annotation_property = self.thing.find_or_create_property(
                "Strava Workout Annotations", "STRAVA_ANNOTATIONS")

        self.disclosure_evaluation_property = self.thing.find_or_create_property(
                "Strava Overview Annotations", "STRAVA_ANNOTATIONS")

       
    
    def download_workout_screenshot(self, ts):
        return self.workout_screenshot_property.read_media('image-png', ts)

    def save_sleep_data_annotations(self, values, ts):
        self.sleep_data_annotation_property.update_values(values=values, time_ms=ts)

    def save_disclosure_evaluation_result(self, values, ts):
        self.disclosure_evaluation_property.update_values(values=values, time_ms=ts)
     
    def save_prolific_id(self, prolific_id, ts):
        values = (prolific_id,)
        self.prolific_id_property.update_values(values=values, time_ms=ts)