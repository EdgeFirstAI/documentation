# Dataset Gallery

To open a dataset gallery, click on the image preview of the dataset card.

{{ figure("../../datasets/assets/management/copied-dataset-result.jpg", "Dataset Card") }}

The gallery is multi-page dashboard split into [sequences](../../datasets/format/structure.md#1-sequence-based-datasets) and [images](../../datasets/format/structure.md#2-image-based-datasets) with a maximum of 40 images shown per page.

{{ figure("../../datasets/assets/management/sample-dataset-sequences.jpg", "Dataset Gallery") }}

## Filters

Filters allow users to select images based on the filter conditions.  The number of images filtered is displayed on the images count.  Filtered images can be copies to another dataset.

{{ figure("../assets/datasets/gallery-filters.png", "Gallery Filters") }}

## Tag an Image

You can create tags for images.  These tags can be used to filter out images of certain tags.  Tags can be added from the "ACTIONS" dropdown and can be filtered using the "IMAGE TAGS" filter.

- Display tags: enable "Show Tags" under "Display Image Options".

{{ figure("../assets/datasets/image-options.png", "Image Options") }}

- Create new tags: click on the first line labeled "Click here to add a new tag".  Then press the ENTER key or click the accept button at the right side of the input field to create the tag.  If any image is selected, this tag will be automatically applied to those images.

{{ figure("../assets/datasets/add-tags.png", "Adding Tags") }}

- Edit existing tags: click on the pencil icon when hovering over a tag name.  Enter the new tag name and click the accept button at the right side of the input.

{{ figure("../assets/datasets/enter-tag-name.png", "Enter Tag Name") }}

- Delete existing tags: click on the (+) icon when hovering over a tag name.  A confirmation popup will open.  Confirming this will remove this tag from the dataset and all applied images.

{{ figure("../assets/datasets/remove-tag.png", "Remove Tag") }}

- Apply and revert tags: at least one image must be selected to apply or revert tags.  Click on any tag under the dropdown to select it.  Applied tags are denoted by a check icon.  To remove the applied tags, click on it again.

## Copy Selected Items

You can copy selected items to another dataset.  This operation can be found under the "ACTIONS" dropdown.  The copy dialog will appear.

{{ figure("../assets/datasets/copy-selected-items.png", "Copy Selected Items") }}

1. Source is auto-filled using the current dataset and first annotation set if applicable.  You can select a different source annotation set.
2. Destination will be defaulted to a new dataset along with any selected annotation set.  You can select another dataset and annotation if needed.
3. Selected file names that will be copied are shown at the bottom.
4. Progress can be tracked in the task progress popup.

## Next Steps

This page has described the features and context of the dataset gallery.  Proceed to the next section for learning more about [annotation sets](annotations.md).
