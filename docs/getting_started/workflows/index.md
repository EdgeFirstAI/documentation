# User Workflows

Edgefirst Studio provides specific workflows tailored towards various user personas depending on the hardware requirements and resources available to the user.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/MmoDCXj72jk?si=I8gTw2VCtcts69ks" title="EdgeFirst Studio Overview" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## User Personas 

The following diagram describes the workflow for identifying the user personas depending on the hardware requirements.

```mermaid
%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
flowchart LR
    %% User Definitions
    user([User])
    platform{Has a platform?}
    edgefirst_platform{Has an EdgeFirst Platform?}
    raivin_platform{Has a Raivin?}
    record{Will use a smartphone to create a dataset?}
    annotate_pd{Will explore annotating datasets?}
    with_lidar{Has LiDAR integrated?}
    tba[TBA]

    tourist([Tourist]):::blue
    tourist_plus([Tourist+]):::teal
    web_user([Web]):::orange
    maivin_user([Maivin]):::green
    raivin_user([Raivin]):::purple
    raivin_lidar_user([LiDAR]):::coral

    classDef blue fill:#d0ecff,font-weight:bold;
    classDef teal fill:#a2e8ed,font-weight:bold;
    classDef orange fill:#ffd699,font-weight:bold;
    classDef green fill:#a9e5bb,font-weight:bold;
    classDef purple fill:#d6c1f5,font-weight:bold;
    classDef coral fill:#ffc2b,font-weight:bold;
    classDef all fill:#f0e6f5,font-weight:bold;

    %% Flowchart
    user --> platform
    platform -- Yes --> edgefirst_platform
    platform -- No --> record
    record -- Yes --> web_user
    record -- No --> annotate_pd
    annotate_pd -- Yes --> tourist_plus
    annotate_pd -- No --> tourist
    edgefirst_platform -- Yes --> raivin_platform 
    edgefirst_platform -- No --> tba
    raivin_platform -- Yes --> with_lidar
    with_lidar -- Yes --> raivin_lidar_user
    with_lidar -- No --> raivin_user
    raivin_platform -- No --> maivin_user
```

!!! warning "PC Requirement"
    It is expected that for all personas identified above, the user has a PC with Wifi access.

We've identified six workflows: Tourist, Tourist+, Web, Maivin, Raivin, LiDAR.  The hardware requirements and the available features increases starting with the Tourist as the most basic. 

| Persona        | Hardware              | Features                                                                |
|----------------|-----------------------|-------------------------------------------------------------------------|
| Tourist        | PC                    | Train, Validate, Deploy Offline                                         |
| Tourist+       | PC                    | Annotate 2D, Train, Validate, Deploy Offline                            |
| Web            | PC + Smartphone       | Record, Annotate 2D, Train, Validate, Deploy Offline                    |
| Maivin         | PC + Maivin           | Record, Annotate 2D, Train, Validate, Deploy on Device                  |
| Raivin         | PC + Raivin w/ Radar  | Record, Annotate 2D + 3D, Train, Validate, Deploy on Device             |
| LiDAR          | PC + Raivin w/ LiDAR  | Record, Annotate 2D + 3D (enhanced), Train, Validate, Deploy on Device  |

## User Journey

The following diagram describes the workflows for each user persona identified above.

```mermaid
%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
%%{init: {"themeVariables": { "fontSize": "40px" }}}%%
flowchart LR
    %% User Definitions
    tourist([Tourist]):::blue
    tourist_plus([Tourist+]):::teal
    web_user([Web]):::orange
    maivin_user([Maivin]):::green
    raivin_user([Raivin]):::purple
    raivin_lidar_user([LiDAR]):::coral

    classDef blue fill:#d0ecff,font-weight:bold;
    classDef teal fill:#a2e8ed,font-weight:bold;
    classDef orange fill:#ffd699,font-weight:bold;
    classDef green fill:#a9e5bb,font-weight:bold;
    classDef purple fill:#d6c1f5,font-weight:bold;
    classDef coral fill:#ffc2b,font-weight:bold;
    classDef all fill:#f0e6f5,font-weight:bold;

    %% Hardware Definitions
    raivin_lidar_hardware[Raivin + LiDAR Quickstart]
    raivin_hardware[Raivin Quickstart]
    maivin_hardware[Maivin Quickstart]

    %% Dataset Definitions
    record_mcap[Record MCAP]
    capture[Take video/images from smartphone]
    snapshot[Create and restore snapshot]
    copy_dataset[Copy public dataset]
    audit_3d[Auto Annotate 3D]
    audit_2d[Auto Annotate 2D]

    %% Model Definitions [train, validate, deploy 2D and 3D]
    train_2d[Train Vision Model]
    validate_2d[Validate Vision Model]
    jupyter_2d[Deploy Vision Model on the PC]
    maivin_2d[Deploy Vision Model on the Maivin]

    train_3d[Train Fusion Model]
    validate_3d[Validate Fusion Model]
    raivin_3d[Deploy Fusion Model on the Raivin]

    %% Flowchart Starting Points
    raivin_lidar_user --> raivin_lidar_hardware --> record_mcap
    raivin_user --> raivin_hardware --> record_mcap
    maivin_user --> maivin_hardware --> record_mcap
    web_user --> capture
    tourist_plus --> copy_dataset
    tourist --> copy_dataset

    %% Flowchart Dataset Processes
    record_mcap --> snapshot 
    snapshot --> audit_2d --> train_2d
    snapshot --Raivin/LiDAR Only--> audit_3d --> train_3d
    capture --> audit_2d
    copy_dataset --Tourist+ Only--> audit_2d 
    copy_dataset --Tourist Only--> train_2d

    %% Flowchart Model Processes
    train_2d --> validate_2d 
    validate_2d --> jupyter_2d
    validate_2d --Maivin/Raivin/LiDAR Only--> maivin_2d
    train_3d --> validate_3d --> raivin_3d

    %% linkStyle 0 stroke:#ff6f61
    %% linkStyle 1 stroke:#ff6f61
```

!!! note
    Labeled arrows suggests that only certain type of users can enter the stages pointed by the arrow.  For example, only Raivin and LiDAR users can "Auto Annotate 3D".

1. [Web Workflow](web.md)

    This workflow is intended for users with a personal computer and a device with a camera with access to Wifi and a web browser.  The examples shown in this workflow will be from a Windows computer and an Android phone for recording images.  To proceed to this workflow, click on the link above.

2. [EdgeFirst Platform Workflow](edgefirst.md)

    This workflow is intended for users with a personal computer with access to Wifi and a web browser and a Maivin or a Raivin platform.  To proceed to this workflow, click on the link above.

!!! note

    The maivin, raivin, and LiDAR persona are currently based on the EdgeFirst Platform Workflow identified as the second workflow above.  Future work will introduce separate workflows for each of these personas to highlight their differences. 