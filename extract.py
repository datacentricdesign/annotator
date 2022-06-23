from dcd.bucket.thing import Thing, Property
import os
import csv


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


def align_values_to(prop1, prop2):
    index = 0
    for values_prop2 in prop2.values:
        if (index >= len(prop1.values) or prop2.values[index][0] != prop1.values[index][0]):
            tmp = [values_prop2[0]]
            for val in range(1,len(prop1.values[0])):
                tmp.append(None)
            prop1.values.insert(index, tmp)
        index = index+1

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

def merge_sleep_data(thing:Thing, from_ts, to_ts):
    property_prolific = thing.find_property_by_name("Prolific ID")
    property_prolific.read(from_ts=from_ts, to_ts=to_ts)

    property_study = thing.find_property_by_name("Study ID")
    property_study.read(from_ts=from_ts, to_ts=to_ts)
    align_values_to(property_study, property_prolific)
    total = merge(property_prolific, property_study)

    property_NDP_Timestamp = thing.find_property_by_name("NDP Timestamp")
    property_NDP_Timestamp.read(from_ts=from_ts, to_ts=to_ts)
    align_values_to(property_NDP_Timestamp, property_prolific)
    total = merge(total, property_NDP_Timestamp)

    property_annotation = thing.find_property_by_name("Sleep Data Annotations")
    property_annotation.read(from_ts=from_ts, to_ts=to_ts)
    align_values_to(property_annotation, property_prolific)
    total = merge(total, property_annotation)

    property_trust = thing.find_property_by_name("Trust Level")
    property_trust.read(from_ts=from_ts, to_ts=to_ts)
    align_values_to(property_trust, property_prolific)
    total = merge(total, property_trust)
    
    property_intimacy = thing.find_property_by_name("Intimacy Level")
    property_intimacy.read(from_ts=from_ts, to_ts=to_ts)
    align_values_to(property_intimacy, property_prolific)
    total = merge(total, property_intimacy)

    property_entertainment = thing.find_property_by_name("Entertainment Level")
    property_entertainment.read(from_ts=from_ts, to_ts=to_ts)
    align_values_to(property_entertainment, property_prolific)
    total = merge(total, property_entertainment)

    property_screenshot = thing.find_property_by_name("Sleep data Screenshot")
    property_screenshot.read(from_ts=from_ts, to_ts=to_ts)
    align_values_to(property_screenshot, property_prolific)
    total = merge(total, property_screenshot)

    print()

    with open('data/sleep_data.csv', 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(total.values)


thing_annotator = Thing()
thing_annotator.describe()
merge_sleep_data(thing_annotator, "2022-06-20 00:00:00", "2022-06-23 00:00:00")
download_media(thing_annotator, "Sleep data Screenshot", "2022-06-20 00:00:00", "2022-06-23 00:00:00")

# merge_strava(thing_annotator, "2022-01-01 00:00:00", "2022-02-18 00:00:00")

# download_media(thing_annotator, "Strava Overview Screenshot", "2022-01-01 00:00:00", "2022-02-18 00:00:00")
# download_media(thing_annotator, "Strava Workout Screenshot", "2022-01-01 00:00:00", "2022-02-18 00:00:00")
