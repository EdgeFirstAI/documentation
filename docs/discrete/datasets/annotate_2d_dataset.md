# Annotate Dataset

Now that you have a dataset in your project, you can start annotating the dataset.  This will briefly show the steps for annotating the dataset, but for an in depth tutorial on the annotation process, please see [Dataset Annotations](../../datasets/tutorials/annotations/index.md).  

To annotate a dataset, first create an annotation set on the dataset card.

<figure markdown="span">
![Annotation Set](../../datasets/assets/annotations/add-annotation-set-button.jpg){ align=center }
<figcaption>Annotation Set</figcaption>
</figure>

A new annotation set was created called "new-annotations".

<figure markdown="span">
![New Annotation Set](../../datasets/assets/annotations/new-annotation-set.jpg){ align=center }
<figcaption>New Annotation Set</figcaption>
</figure>

Next, open the dataset gallery, by clicking on the gallery button ![Gallery Button](../../assets/buttons/studio-gallery-button.jpg) on the top left of the dataset card.  The dataset will contain sequences (video) ![Sequences Icon](../../assets/buttons/studio-sequence-icon.jpg) and images.  Click on any sequence card to start [annotating sequences](../../datasets/tutorials/annotations/automatic.md#semi-automatic-ground-truth-generation). 

<figure markdown="span">
![Coffee Cup Gallery](../../datasets/assets/annotations/coffee-cup-gallery.jpg){ align=center }
<figcaption>Coffee Cup Gallery</figcaption>
</figure>

On the top navbar, switch to the right annotation set.

<figure markdown="span">
![Switch Annotation Set](../../datasets/assets/annotations/switch-annotation-sets.jpg){ align=center }
<figcaption>Switch Annotation Set</figcaption>
</figure>

[Start the AGTG server](../../datasets/tutorials/annotations/automatic.md#initialize-agtg-server) by clicking on the "AI Segment Tool" and follow the prompts as indicated.

<figure markdown="span">
![Auto Segment Mode](../../datasets/assets/annotations/automatic/agtg-segment-tool.jpg){ align=center }
<figcaption>Auto Segment Mode</figcaption>
</figure>

Once the AGTG server has started, go ahead and [annotate the starting frame](../../datasets/tutorials/annotations/automatic.md#annotate-starting-frame).

<figure markdown="span">
![AGTG Initial Prompts](../../datasets/assets/annotations/automatic/agtg-prompts.jpg){ align=center }
<figcaption>AGTG Initial Prompts</figcaption>
</figure>

Once the starting frame has been annotate, go ahead and [propagate the annotations](../../datasets/tutorials/annotations/automatic.md#propagate) throughout the rest of the frames.

<figure markdown="span">
![Propagation Process](../../datasets/assets/annotations/automatic/propagation-process.jpg){ align=center }
<figcaption>Propagation Process</figcaption>
</figure>

Repeat the steps for all the sequences in the dataset.  For the case of individual images, the same steps apply except there is no propagation step.  More details are provided in the [manual annotations](../../datasets/tutorials/annotations/manual.md#add-2d-annotations). 
