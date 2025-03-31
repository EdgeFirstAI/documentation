# Studio Client

The EdgeFirst Studio Client, `edgefirst-client`, provides an API and command-line interface (CLI) into the EdgeFirst Studio Server.  This client provides programmatic and command-line access to many of the features of the EdgeFirst Studio.  

This page describes the command-line interface, the API is documented under the Developer Guide.

A summary of the core features is listed below:

- Project List & Search
- Dataset List & Search & Export
- Annotations Listing & Export to JSON and Arrow
- Snapshot Download & Upload & Restore to Dataset (including Auto-Annotations)
- Trainer List & Search
- Trainer Session List & Search & Artifacts Download
- Validator List & Search

## Installation

The Python package includes the command-line application and is an easy way to install the binary.

`pip install edgefirst-client`

!!! tip "Included with EdgeFirst Middleware"

    The `edgefirst-client` is installed as part of the standard EdgeFirst Middleware installation, no additional setup is required.    

Once installed you can confirm you can communicate with the EdgeFirst Studio Server with the version command.

```
$ edgefirst-client version
Deep View Enterprise 3.6.6a
```

## Authentication

Authentication to the EdgeFirst Studio Server is done using the standard login you would use from the web interface.  To avoid having to type your username and password each time an authentication token can be generated and saved using the `login` command.

```
$ edgefirst-client login
Username: user
Password: ****
```

This will generate an authentication token which remains valid for 7 days and save it in the edgefirst-client configuration file.  At any time you can use the `logout` command to forget the token and remove it from the configuration file.

## Usage

Usage information is provided by the `help` command.

```shell
$ edgefirst-client help
Usage: edgefirst-client [OPTIONS] <COMMAND>

Commands:
  version            Returns the Deep View Enterprise Server version
  login              Login to the Deep View Enterprise Server with the provided username and password.  The token is stored in the application configuration file
  logout             Logout by removing the token from the application configuration file
  token              Returns the DVE authentication token for the provided username and password.  This would typically be stored into the DVE_TOKEN environment variable for subsequent commands to avoid re-entering username/password
  projects           List all projects available to the authenticated user
  project            Retrieve project information for the provided project ID
  find-project       Find a project by name
  datasets           List all datasets available to the authenticated user.  If a project ID is provided, only datasets for that project are listed
  dataset            Retrieve dataset information for the provided dataset ID.  The cloud key can be printed with the --cloud-key option, this requires additional AWS S3 permissions to access the bucket
  find-dataset       Find a dataset by name.  If a project ID is provided, only datasets for that project are searched.  A project name can also be provided which will be used to find the project ID
  download-dataset   Download a dataset to the local filesystem.  The dataset ID is required along with an optional output file path, if none is provided the dataset is downloaded to the current working directory
  annotation-sets    List available annotation sets for the provided dataset ID
  annotations        Fetch annotations for the provided dataset and annotation set ID. The retrieved annotations are filtered by annotation type. The annotations are printed in JSON format
  snapshots          List available snapshots
  snapshot           Retrieve snapshot information for the provided snapshot ID
  find-snapshots     Find snapshots containing the provided description
  create-snapshot    Create a new snapshot from the provided path which can be a file or directory.  The snapshot name will be the base name of the path
  download-snapshot  Downloads a snapshot to the local filesystem.  The snapshot ID is required along with an optional output file path, if none is provided the snapshot is downloaded to the current working directory
  restore-snapshot   Restore a snapshot to the provided project ID.  The snapshot ID is required along with optional flags to restore the depth generator and AGTG pipeline.  The dataset name and description can also be provided to override the snapshot name, otherwise the snapshot name is used and the description is set to the snapshot timestamp
  trainers           List training experiments for the provided project ID (optional).  The trainers are groups of "experiments" in mlflow parlance, training jobs can be queried through the trainer-session commands
  trainer            Retrieve trainer information for the provided trainer ID
  trainer-sessions   List training sessions for the provided trainer ID (optional).  The sessions are individual training jobs that can be queried for more detailed information
  trainer-session    Retrieve training session information for the provided session ID.  The trainer session ID can be either be an integer or a string with the format t-xxx where xxx is the session ID in hex as shown in the DVE UI
  download-artifact  Download an artifact from the provided session ID.  The session ID can be either be an integer or a string with the format t-xxx where xxx is the session ID in hex as shown in the DVE UI.  The artifact name is the name of the file to download.  The output file path is optional, if none is provided the artifact is downloaded to the current working directory
  help               Print this message or the help of the given subcommand(s)

Options:
      --server <SERVER>      DVE Server Name
      --username <USERNAME>  DVE Username
      --password <PASSWORD>  DVE Password
      --token <TOKEN>        DVE Token
  -h, --help                 Print help
  -V, --version              Print version
```
