# Matching and Classification Rules

This section describes the rules governing the matching algorithm in EdgeFirst Validator for object detection.  The matching algorithm is responsible for matching the ground truths to the detections based on the best overlap (IoU + label) and allows classification of detections into true positives, false positives, and false negatives.

## Rule 1: Requirements of True Positives

Recap: A detection can be a true positive if it meets the requirements described below.

* The detection label matches the ground truth label.
* The detection and ground truth IoU >= IoU threshold (0.50-0.95).
* The detection confidence score >= score threshold (NMS).

## Rule 2: Requirements of False Positives

Recap: False positives are categorized into localization and classification.

*Classification false positives* meet the requirements described below.

* The detection label does not match the ground truth label.
* The detection and ground truth IoU >= IoU threshold.
* The detection confidence score >= score threshold (NMS).

*Localization false positives* meet the requirements described below.

* The detection and ground truth IoU < IoU threshold.
* The detection does not overlap any ground truth (IoU = 0).

## Rule 3: Requirements of False Negatives

* Any ground truth where the IoU < IoU threshold.
* Any ground truth that does not overlap a detection.

## Rule 4: Unique Matches

There exists only one detection (true positive or classification false positive) that is matched per ground truth.

### Rule 4.1: True Positive Count

The number of true positives should not exceed the number of ground truths nor the number of predictions.

* Each ground truth may have at most, one true positive.
* Each prediction may have at most, one true positive.

### Rule 4.2: Classification False Positive Count

The number of classification false positives should not exceed the number of ground truths nor the number of predictions.

* If a ground truth does not have a true positive, it may have at most, one classification false positive.
* If a prediction does not have a true positive, it may have at most, one classification false positive.

### Rule 4.3: Localization False Positives Count

For a dataset without any ground truth to detection overlaps, the number of localization false positives should be the total number of predictions.

### Rule 4.4: False Negatives

For cases with no model detections, the number of false negatives is equal to the number of ground truth annotations.

## Rule 5: Prioritization Cases

If a detection meets the requirements of a true positive, it will be matched to the ground truth.  Otherwise, if a detection meets the requirements of a classification false positive, it will be matched to the ground truth.  Otherwise, it is a localization false positive.  Consider the following cases.

### Rule 5.1: Matching Labels Are Prioritized Over IoU

Considering two detections and one ground truth, the detection with a lower IoU, but with the same label as the ground truth should be matched over a detection with a higher IoU, but with a mismatching label as long as both detections have IoU >= IoU threshold.

The following images provides visualization to this rule.  The IoU threshold is set to 0.10 and the score threshold is set to 0.50 in these cases.

{{ figure("../../assets/metrics/rule_5.1_000000000127.png", "Playing Cards v7; 000000000127.png") }}

{{ figure("../../assets/metrics/rule_5.1_000020.png", "Playing Cards; 000020.png") }}

Otherwise, if these detections, are lower than the IoU threshold, they will be regarded as localization false positives and one false negative from the ground truth as shown below.

{{ figure("../../assets/metrics/rule_5.1_000000000127_fp.png", "000000000127.png; IoU threshold = 0.90") }}

{{ figure("../../assets/metrics/rule_5.1_000020_fp.png", "000020.png; IoU threshold = 0.90") }}

### Rule 5.2: Prioritization of Highest IoU Matches

For cases where multiple detections have labels that matches the ground truth, the highest IoU is matched.

The following image shows visualization of this rule where the IoU threshold is set to 0.10 and the score threshold is set to 0.50.

{{ figure("../../assets/metrics/rule_5.2_000000000145.png", "Playing Cards V7; 000000000145.png") }}

These detections have the same label as the ground truth, but the IoU varies, each detection overlaps the ground truth.  The greatest overlap is taken as the match.  Since this match meets the criteria of a true positive, it is classified as such.

### Rule 5.3: Matching Labels, Highest IoU Matches

For cases that concerns both scenarios as the rules described above.  A match is based on a matching label and the highest IoU with the ground truth if multiple detections are present with varied labels and varied IoUs.

The following image shows a visualization of this rule following the same IoU threshold set to 0.10 and the score threshold set to 0.50.

{{ figure("../../assets/metrics/rule_5.3_000000000134.png", "Playing Cards v7; 000000000134.png") }}

In this case, matching labels are prioritized and the highest IoU is taken as the match.

### Rule 5.4: Mismatching Labels, Highest IoU Matches

For cases of having detections with matching labels as the ground truth, but do not meet the IoU threshold requirements, the detections with mismatching labels are matched if it meets the IoU threshold requirements.  

The following image with visualization shows an IoU threshold set to 0.50.

{{ figure("../../assets/metrics/rule_5.4_000000000134.png", "Playing Cards v7; 000000000134.png") }}

Despite a detection with a matching label of "ace" as the ground truth being present, it is still regarded as a localization false positive since it does not meet the IoU requirements.  The detection with the highest IoU is matched instead which is with the label "king".

Otherwise, if all detections do not meet the IoU threshold requirements, they will be treated as localization false positives and one false negative for the ground truth as shown in the image results below.

{{ figure("../../assets/metrics/rule_5.4_000000000134_locfp.png", "Playing Cards v7; 000000000134.png") }}

### Rule 5.5: Matches Meets IoU Threshold Requirements

Any detections that do not overlap any ground truth or any detections with IoU < IoU threshold will be regarded as localization false positives.

{{ figure("../../assets/metrics/rule_5.5_000000000148.png", "Playing Cards v7; 000000000148.png") }}

## Conclusion

This article has shown the rules established in EdgeFirst Validator that governs the behaviour of the matching and classification algorithms to process the raw detections into their classifications of true positives, false positives, and false negatives.  Rules 1-3 shows the requirements of these classifications.  Rule 4 describes the limits to the count of these classifications.  Rule 5 shows the prioritization of matches to ensure classification requirements are met by prioritizing finding of true positives first, then classification false positives, and then localization false positives.
