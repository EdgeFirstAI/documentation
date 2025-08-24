# Model Metadata

This page will describe the meta data embedded in model files.  The model metadata contains information for retracing how the model was created in EdgeFirst Studio and additional information for decoding the model outputs. 

## Reading Metadata

A TFLite model is in the Zip format file that embeds the files `config.yaml` and `labels.txt`.  ONNX models supports embedded metadata directly into the model which merges the contents of both `config.yaml` and `labels.txt`.

Reading these files can be done using the python snippets below.

=== "config.yaml"

    ```python
    if zipfile.is_zipfile(model_path):
            with zipfile.ZipFile(model_path) as zip_ref:
                if "config.yaml" in zip_ref.namelist():
                    with zip_ref.open("config.yaml") as f:
                        yaml_text = f.read().decode("utf-8")
                        metadata = yaml.safe_load(yaml_text)
                        return metadata
        return None
    ```

=== "labels.txt"

    ```python
    def get_labels(model_path):
        labels = []
        if zipfile.is_zipfile(model_path):
            with zipfile.ZipFile(model_path, 'r') as zip_ref:
                if "labels.txt" in zip_ref.namelist():
                    with zip_ref.open("labels.txt") as file:
                        content = file.read().decode('utf-8').strip()
                        labels = [line for line in content.splitlines() 
                                if line not in ["\n", "", "\t"]]
        return labels
    ```

The `labels.txt` file is a text file that lists all the labels in the dataset that the model was trained on.  The model outputs indices which can be converted into the string representation using this file.  As an example, the contents of this file would appear like the [COCO labels](../../datasets/coco/index.md#coco-labels).

The `config.yaml` is formatted like a dictionary and contains more information on how the model was trained in EdgeFirst Studio and how the outputs can be decoded into boxes, scores, and/or masks. This file contains the following sections below.

```
augmentation:
    # Provides the probabilities on the various augmentation techniques used during training.
deployment:
    # Provides the name & description set in EdgeFirst Studio.
export:
    # Provides export information for quantizing float ONNX into TFLite.
host:
    # Server specific properties.
input:
    # Model input details such as the shape and type.
model:
    # Model specific properties such as the tasks (detection + segmentation), weights, size, etc.
optimizer:
    # Optimizer settings used during training such as the learning rate, optimizer type, etc.
outputs:
    # Model outputs that provides information for decoding the outputs (if necessary).
trainer:
    # Trainer settings such as the number of epochs, batch size, etc.
validation:
    # Validation settings used during training such as the NMS thresholds used.
```

### Augmentation

This section in the metadata lists the augmentation techniques and the probabilities used for each technique during training.  More information can be found for these [augmentation techniques](../augmentations.md). 

```
augmentation:
    random_blur: 0
    random_brightness_contrast: 0
    random_clahe: 0
    random_dropout: 0
    random_grayscale: 0
    random_hflip: 0
    random_hsv: 0
    random_mosaic: 0
    random_shift_scale_rotate: 0
```

### Deployment

This section of the metadata stores information specified in EdgeFirst Studio when specifying the name, description, and model upon [creating the training session](../modelpack/training.md#create-training-session).

```
deployment:
    author: Au-Zone Technologies
    description: Training on local machine
    model_name: modelpack-legacy
    name: null
```

### Export

This section of the metadata stores the export information for exporting the float ONNX model into a quantized TFLite.

```
export:
    calibration_samples: 100  
    export: true              
    export_input_type: uint8  
    export_output_type: uint8 
    tensor_quantization: true 
```

* calibration_samples: number of calibration samples. If the number if larger than the dataset then the whole dataset is used.
* export: if set to true, the model will be quantized. 
* export_input_type: input type.
* export_output_type: output type.
* tensor_quantization: per-tensor quantization. 

### Host

This section of the metadata stores the information related to the training session in EdgeFirst Studio. 

```
host:
    host: null
    session: null
    username: null
```

* host: EdgeFirst Studio server used for creating the training session from "test", "stage", "saas".
* session: train session-id in EdgeFirst Studio.
* username: user's username used to login to EdgeFirst Studio.

### Input

This section of the metadata describes the model input shape and type.

```
input:
    color_adaptor: rgb   
    size: 640x640        
```

* color_adaptor: camera adaptor (rgb, rgba, yuyv).
* size: input resolution (width, height) separated by x.

### Model

```
model:
    activation: relu6    
    anchors:            
    - - - 35
        - 42
        - - 57
        - 89
        - - 125
        - 126
    - - - 125
        - 126
        - - 208
        - 260
        - - 529
        - 491
    autoanchors: false      
    backbone: cspdarknet19  
    class_frequency:        
    - 0.9476275444030762
    - 0.9623422622680664
    - 1.0468722581863403
    - 1.1268153190612793
    - 1.0648597478866577
    - 1.118679404258728
    - 1.0797010660171509
    - 1.083476185798645
    - 0.8955901861190796
    - 0.8704331517219543
    - 1.0193229913711548
    - 0.8728850483894348
    - 0.9113947153091431
    classification: false     
    detection: true           
    segmentation: false
    cls_weights: 1.0          
    iou_weights: 1.0          
    obj_weights: 1.0          
    iou_loss: ciou            
    encoding_threshold: 0.4   
    model_name: cspdarknet19-detection-nano-rgb   
    model_size: nano         
    preprocessing: unsigned   
    reduction: mean           
    seg_weights: 1.0         
    space_to_depth: false     
    space_to_depth_kernel: null 
    split_decoder: true       
    task: detection           
    use_iou_encoding: false
```

* activation: main activation used in the model.
* anchors: training anchors with shape (r, num_anchors, 2) where num_anchors is usually 3 and r is the number of outputs (2, 3, 2).
* autoanchors: this parameter is used to recompute the anchors before training.
* backbone: backbone name.
* class_frequency: dataset Statistics. Used for class imbalance.
* classification: specify if the model performs classification tasks.
* detection: specify if the model performs detection tasks.
* segmentation: specify if the model performs segmentation tasks.
* cls_weights: weights used for box classification.
* iou_weights: weights for IoU loss.
* obj_weights: objectness weights.
* iou_loss: IoU loss function.
* encoding_threshold: used when IoU encoding is enabled.
* model_name: This name is the one used for naming the keras model.
* model_size: model expansion.
* preprocessing: input preprocessing function/normalization.
* reduction: specifies how the losses are collected.
* seg_weights: this weight is a penalty for the segmentation loss when training multitask (detection + segmentation) models.
* space_to_depth: enables Focus layer.
* space_to_depth_kernel: used in the future for the Focus layer to reduce by 2, 4, 8, etc...
* split_decoder: leave decoder outside of the model (model has to be decoded by the inference runner).
* task: model task capabilities (classification, detection, segmentation, or multitask). String value for naming the task.
* use_iou_encoding: specify to use IoU encoding. 

### Optimizer

This section of the metadata describes the optimizer settings during training.

```
optimizer:
    beta_1: 0.9
    beta_2: 0.998
    learning_rate: 0.001
    optimizer: adamw
    warmup_epochs: 3
    warmup_learning_rate: 1.0e-05
    weight_decay: 0.01
```

* beta_1: Exponential decay rate for the **first moment estimate** (mean of gradients). Helps stabilize training.  Default for Adam.
* beta_2: Exponential decay rate for the **second moment estimate** (variance of gradients). Higher value smooths out the learning.  Often set between 0.98–0.999.
* learning_rate: Base learning rate — controls how much the model's weights are updated at each training step.
* optimizer: Specifies the use of **AdamW** optimizer, a variant of Adam that decouples weight decay from gradient updates.  Often preferred for transformer-based models and large-scale training.
* warmup_epochs: Number of initial epochs to **gradually increase** the learning rate from `warmup_learning_rate` to `learning_rate`.  Helps stabilize early training.
* warmup_learning_rate: Initial learning rate at the start of training, used during warmup phase.  Usually set very low to avoid drastic weight updates early on.
* weight_decay: Strength of L2 regularization applied to weights (but decoupled from gradient updates in AdamW).  Helps prevent overfitting.


### Outputs

This section describes the model outputs and often contains information used for decoding the outputs into meaning boxes, classes, scores, or masks.

```
outputs:        
- anchors:      
  - - 0.0546875
    - 0.065625
  - - 0.0890625 
    - 0.1390625
  - - 0.1953125
    - 0.196875
  decode: true    
  decoder: modelpack 
  dtype: uint8      
  index: 90         
  name: PartitionedCall:0 
  output_index: 1
  quantization:           
  - 0.17631953954696655   
  - 198                   
  shape:                  
  - 1
  - 40
  - 40
  - 54
  stride:                 
  - 16
  - 16
  type: detection         
- anchors: 
  - - 0.1953125
    - 0.196875
  - - 0.325
    - 0.40625
  - - 0.8265625
    - 0.7671875
  decode: true
  decoder: modelpack
  dtype: uint8
  index: 89
  name: PartitionedCall:1
  output_index: 0
  quantization:
  - 0.17046131193637848
  - 208
  shape:
  - 1
  - 20
  - 20
  - 54
  stride:
  - 32
  - 32
  type: detection
```

* anchors: optional value that stores the anchors for this resolution if decode is set to true. Anchors are normalized from 0..1 to guarantee normalized boxes.
* decode: specify to true if the output should be decoded.
* decoder: keyword to specify the type of modelpack decoder needed to decode the outputs.
* dtype: output type
* index: tensor index for this output to retrieve the tensor values.
* name: name given to the output by tflite converter.  This could be null if non-existent.
* output_index: output index for the output.
* quantization: quantization parameters which contains the `scale` and `zero_point` values in this order.
* shape: the model output shape.  Typically the grid resolution for non-decoded outputs. 
* stride: contraction factor.
* type: for non-decoded outputs this can either be "detection" or "segmentation".  For decoded outputs, this can be "boxes", "scores", "mask".

### Trainer

This section of the metadata describes additional training parameters set for training the model in EdgeFirst Studio.

```
trainer:
    batch_size: 10
    checkpoint_path: artifacts/metadata/detection/nano-320x320
    epochs: 100
    weights: coco
```

* batch_size: the number of training samples used in one forward/backward pass.  A small batch size (like 10) uses less memory but can result in noisier gradient updates.
* checkpoint_path: the directory where model checkpoints (saved model weights, config, etc.) are stored during training. Useful for resuming training or evaluation.
* epochs: the number of complete passes through the entire training dataset.  More epochs allow the model to learn better — but too many can cause overfitting.
* weights: indicates that training should start from pretrained weights based on the COCO dataset (e.g., a model pretrained on object detection using MS COCO).  This helps the model learn faster and generalize better, especially with limited data.

### Validation

This section of the metadata describes the validation settings used for validating the performance of the model at the end of each epoch during training.

```
validation:
    skip_validation_steps: 1
    validation_iou: 0.1
    validation_threshold: 0.025
```

* skip_validation_steps: the number of steps to skip validation which is typically used during early stages of training where the model is not mature enough to make proper predictions.
* validation_iou: the NMS IoU threshold.  A smaller value is stricter which indicates that a small intersection is needed to be considered a duplicate prediction.
* validation_threshold: the NMS score threshold.  A higher value is stricter which indicates that predictions needs higher confidence to be considered a valid prediction. 

## Adding/Updating Metadata

If a TFLite model already contains a `config.yaml` file, this can be updated with the `zip` command in linux. `zip -u <mymodel.tflite> <path to the new config.yaml>`.
