# The Top Ribbon

The ribbon at the top of the web interface is available on every page of the web interface.  The following elements are available on every page of the device's web interface.

1. On the left, the "Home" button with the Au-Zone icon, which will return the user to the Main Page
2. In the middle, the title of the current page
3. On the right side, we first have the Recording Indicator, shown as a gray oval with "REC" when not recording from the sensors and a red oval when recording
4. The MCAP Details Modal button, which opens the MCAP Modal
5. The EdgeFirst Studio button, which shows whether the device is logged in to EdgeFirst Studio and opens the login dialog used for [uploading recordings](../../perception/data_collection/publishing.md#method-1-upload-from-the-web-ui)
6. The System Status Indicator and Dropdown button
7. The theme toggle switching the interface between light, dark, and automatic modes
8. The farthest rightmost button, with the gear icon, is the Settings Button which will take you to the [Settings Page](../../platforms/configuration/index.md)

Notifications such as the outcome of saving a configuration page or starting a recording appear as cards below the ribbon.  Errors stay until dismissed while informational notifications clear on their own.

# The MCAP Modal

The MCAP Modal is the interface to manage MCAP recordings, including getting information about recorded MCAP files, disk usage, deletion, downloading files, uploading files to EdgeFirst Studio, and replaying files on the device.  More information about the MCAP Modal and recording MCAPs is in the [Recording section](../../perception/data_collection/recording.md)

{{ figure("/platforms/assets/setup/quickStart-mcap.png", "A recorded MCAP file") }}

# System Status Indicator

Mousing over the System Status Indicator field will give a brief summary of any problems.  

{{ figure("/platforms/assets/setup/quickStart-statusDropDownGood.png", "Dropdown reporting good") }}

{{ figure("/platforms/assets/setup/quickStart-statusDropDownDegraded.png", "Dropdown reporting bad") }}

More on these status can be found in the [Status Monitoring section](../../perception/data_collection/replay.md#status-monitoring).

Clicking on the indicator will bring up the Service Status Modal, which contains a list of services and, if available, clickable gear icons that link to the service's configuration page.

{{ figure("/platforms/assets/setup/quickStart-serviceStatusModal.png", "Service Status Modal") }}
