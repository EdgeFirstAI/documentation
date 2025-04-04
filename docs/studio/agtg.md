# Automatic Ground Truth Generation (AGTG)

AGTG allows datasets to have annotation populated on a dataset with minimal human interaction. There are two modes of operation

1. Background Operation: this is invoked at the time of importing the dataset
2. Semi-automatic: users can select portions of dataset sequenced and manually trigger AI assisted annotation

## Fully Automatic Ground Truth Generation

This functionality is available at the time of restoring a snapshot. To invoke this import/create a snapshot and then enable AGTG while restoring the snapshot. Please refer to [Restoring a snapshot](snapshots.md) 

## Semi-Automatic Ground Truth Generation

This process is used to generate 2D Bounding boxes, 2D segmentations and 3D bounding boxes using AI assisted pipelines in DVE

### Starting an AGTG Server
1. Select Cloud Instances dashboard from teh apps menu

![alt text](assets/cloud-instances.png)

2. Click on Start Button
3. Enter A desired name and select AI Assisted Ground Truth

![alt text](assets/launch-ai-server.png)
4. This will create a server. Please refresh to see the status of teh server. The server takes about 5 to 10 minutes to fully initialize.
5. Once initialized, it is ready for usage in next steps.

### Creating AI Assisted Annotations

1. Open a database and go to its gallery
2. Click on a sequence that is intended to be edited
3. Go to the frame where editing begins
4. Enable the editing of annotations:

![alt text](assets/edit-annotations.png)

5. Select Video Segment Tool

![alt text](assets/video-segment-tool.png)

6. Select the AGTG server (as started above) if not already selected
7. Click INITIALIZE STATE. Bt default all frames of the sequence are selected - if only a portion of sequence is to be edit then enter teh starting and ending frame numbers. This will decrease the initialization time.
8. Once initialized, the first object is created without  any segmentation masks. The explanation of icons on teh object card is as follows:

![alt text](assets/ai-segment-options.png)

9. Select an object on the image using rectangle or inclusion points. 
10. The object should be segmented

![alt text](assets/segmented-annotation.png)

11. Click PROPAGATE.
12. This will start a counter and propagate the object from starting frame to the ending frame
13. Scroll through teh frames to see if teh propagation is correct
14. If satisfied, click on the SAVE PENDING SEGMENTATIONS to store the annotations to the dataset
15. If the dataset has LIDAR, then 3D bounding boxes are also created for teh same object
16. Repeat for other object as necessary
