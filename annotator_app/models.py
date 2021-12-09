
from dcd.bucket.thing import Thing

class Bucket:

    def __init__(self):
        self.thing = Thing()

        self.workout_screenshot_property = self.thing.find_or_create_property(
                "Strava Workout Screenshot", "IMAGE_PNG")

        self.workout_screenshot_property.describe()

        self.workout_annotation_property = self.thing.find_or_create_property(
                "Strava Workout Annotation", "TEXT")

        self.workout_annotation_property.describe()

    def upload_workout_screenshot(self, ts, file_name):
        values = (100,100)
        self.workout_screenshot_property.update_values(values, ts, file_name=file_name)

    def download_workout_screenshot(self, ts):
        return self.workout_screenshot_property.read_media('image-png', ts)

    def save_workout_annotation(self, values, ts):
        self.workout_annotation_property.update_values(values=values, time_ms=ts)