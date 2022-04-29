# Create your models here.
from django.db import models
from dcd.bucket.thing import Thing
import environ

env = environ.Env()
environ.Env.read_env(env_file=".env")
STUDY_ID = env("STUDY_ID")

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
    
    