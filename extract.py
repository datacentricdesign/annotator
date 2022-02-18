from dcd.bucket.thing import Thing, Property
import os
import csv

thing_annotator = Thing()

thing_annotator.describe()

def download_media(thing: Thing, property_name: str, from_ts, to_ts):
    property = thing.find_property_by_name(property_name)
    property.read(from_ts=from_ts, to_ts=to_ts)

    dir_path = f"data/{property.property_id}"
    if os.path.exists(dir_path) is False:
        os.mkdir(dir_path)
    for values in property.values:  
        file_content = property.read_media("image-png",values[0])
        file_path = f"data/{property.property_id}/{values[0]}.png"
        # Finally we can write the content into a file
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(f"data/{property.property_id}/{values[0]}.png",'wb') as f:
            f.write(file_content)


def merge(prop1:Property, prop2:Property):
    """
        Create a new Property with id and name of form "prop1+prop2",
        concat dimension and values (MUST have same number of rows)
        and return this new property
    """
    prop3 = Property(
        property_id=f"{prop1.property_id}+{prop2.property_id}",
        name=f"{prop1.name}+{prop2.name}")

    # Concat dimensions
    prop3.type = {}
    prop3.type["dimensions"] = prop1.type["dimensions"] + prop2.type["dimensions"]
    # Remove timestamps from property 2
    values2_no_ts = map(lambda x: x[1:], prop2.values)
    # concat property 1 and 2 (only 1 timestamp from prop 1)
    prop3.values = [a+b for a, b in zip(prop1.values, values2_no_ts)]

    return prop3

def merge_strava(thing:Thing, from_ts, to_ts):
    property_prolific = thing.find_property_by_name("Prolific ID")
    property_prolific.read(from_ts=from_ts, to_ts=to_ts)

    property_workout_annotations = thing.find_property_by_name("Strava Workout Annotations")
    property_workout_annotations.read(from_ts=from_ts, to_ts=to_ts)
    property_workout_annotations.align_values_to(property_prolific)
    total = merge(property_prolific, property_workout_annotations)

    property_overview_annotations = thing.find_property_by_name("Strava Overview Annotations")
    property_overview_annotations.read(from_ts=from_ts, to_ts=to_ts)
    property_overview_annotations.align_values_to(property_prolific)
    total = merge(total, property_overview_annotations)

    property_workout_annotation_metrics = thing.find_property_by_name("Strava Workout Annotation Metrics")
    property_workout_annotation_metrics.read(from_ts=from_ts, to_ts=to_ts)
    property_workout_annotation_metrics.align_values_to(property_prolific)
    total = merge(total, property_workout_annotation_metrics)

    with open('data/all_data.csv', 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(total.values)

merge_strava(thing_annotator, "2022-01-01 00:00:00", "2022-02-18 00:00:00")

download_media(thing_annotator, "Strava Overview Screenshot", "2022-01-01 00:00:00", "2022-02-18 00:00:00")
download_media(thing_annotator, "Strava Workout Screenshot", "2022-01-01 00:00:00", "2022-02-18 00:00:00")
