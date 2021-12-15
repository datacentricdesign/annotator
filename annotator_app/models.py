
from dcd.bucket.thing import Thing

class Bucket:

    def __init__(self):
        self.thing = Thing()

        self.workout_screenshot_property = self.thing.find_or_create_property(
                "Strava Workout Screenshot", "IMAGE_PNG")

        self.overview_screenshot_property = self.thing.find_or_create_property(
                "Strava Overview Screenshot", "IMAGE_PNG")

        self.prolific_id_property = self.thing.find_or_create_property(
                "Prolific ID", "TEXT")

        self.workout_annotations_property = self.thing.find_or_create_property(
                "Strava Workout Annotations", "STRAVA_ANNOTATIONS")

        self.overview_annotations_property = self.thing.find_or_create_property(
                "Strava Overview Annotations", "STRAVA_ANNOTATIONS")

        self.workout_annotation_metrics_property = self.thing.find_or_create_property(
                "Strava Workout Annotation Metrics", "STRAVA_WORKOUT_ANNOTATION_METRICS")

    def upload_workout_screenshot(self, ts, file_name):
        values = (100,100)
        self.workout_screenshot_property.update_values(values, ts, file_name=file_name)

    def upload_overview_screenshot(self, ts, file_name):
        values = (100,100)
        self.overview_screenshot_property.update_values(values, ts, file_name=file_name)

    def download_workout_screenshot(self, ts):
        return self.workout_screenshot_property.read_media('image-png', ts)

    def download_overview_screenshot(self, ts):
        return self.overview_screenshot_property.read_media('image-png', ts)

    def save_workout_annotations(self, values, ts):
        self.workout_annotations_property.update_values(values=values, time_ms=ts)

    def save_overview_annotations(self, values, ts):
        self.overview_annotations_property.update_values(values=values, time_ms=ts)
    
    def save_workout_annotation_metrics(self, values, ts):
        self.workout_annotation_metrics_property.update_values(values=values, time_ms=ts)
    
    def save_prolific_id(self, prolific_id, ts):
        values = (prolific_id,)
        self.prolific_id_property.update_values(values=values, time_ms=ts)