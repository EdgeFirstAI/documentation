# Getting Started

![EdgeFirst Studio](assets/studio.png#only-light)
![EdgeFirst Studio](assets/studio-dark.png#only-dark)

Welcome to EdgeFirst Studio (formerly Deep View Enterprise)!  This guide will introduce you to the components of the EdgeFirst AI Ecosystem.

!!! tip "Need Help?"
    📬 Have questions or ran into an issue?  
    Feel free to [email our support team](mailto:support@edgefirst.ai) — we’re here to help!

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/HaiYg6Dk57Y" title="EdgeFirst Studio Introduction" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## EdgeFirst Platforms Quickstart

If you have recently received one of these EdgeFirst Platforms, you should first start with
the [EdgeFirst Platforms Quickstart](platforms/quickstart.md) and then come back once you're ready to get started with EdgeFirst Studio.

**[Maivin 1](platforms/index.md)** | **[Maivin 2](platforms/index.md)** | **[Raivin](platforms/index.md)**
:------------------:|:------------------:|:------------------:
[![Maivin 1](platforms/assets/maivin-1.png)](platforms/index.md) | [![Maivin 2](platforms/assets/maivin-2.png)](platforms/index.md) | [![Raivin](platforms/assets/raivin.png)](platforms/index.md)

!!! tip
    Though not required, where appropriate, we recommend you to follow along with an appropriate edge device to test the models on the actual hardware.

## EdgeFirst Studio Quickstart

This section describes the steps for onboarding new users to EdgeFirst Studio by creating their account, logging into EdgeFirst Studio, and creating their first project. 

### Sign Up

1. If you haven't already created an EdgeFirst Studio Account, start by [creating an account][signup]. 

2. When creating your account, enter the required fields denoted by the asterisk (*) and then create your account once completed.

    <figure markdown="span">
    ![Create a New Account](assets/signup-page.jpg){ align=center }
    <figcaption>Create a New Account</figcaption>
    </figure>

3. An email will be sent to verify the email you provided. Go ahead and click on the link provided to verify your email.

    <figure markdown="span">
    ![Email Verification](assets/email-verification.jpg){ align=center }
    <figcaption>Email Verification</figcaption>
    </figure>

4. Once the email is verified, you can now [login][login] to EdgeFirst Studio.

5. When logging in, enter your username and password you specified. Next click the *SIGN IN* button to sign in.

    <figure markdown="span">
    ![Login Page](assets/login-page.jpg){ align=center }
    <figcaption>Login Page</figcaption>
    </figure>

6. Once logged in to EdgeFirst Studio, you will be greeted with the following [Projects](./studio/projects.md) page.

    <figure markdown="span">
    ![Starting Page](assets/studio-from-scratch.jpg){ align=center }
    <figcaption>Projects Splash Page</figcaption>
    </figure>

### Initial Steps

Now that you are in the *Projects* or Main page, you will see a public project called "Sample Datasets" containing public datasets and completed experiments. More information about this project will be provided in the [EdgeFirst Studio Overview](getting_started/workflows.md). 

For now, let's start by creating your first project since this is required in future tutorials. You can create a new project by clicking on the "Create" button on the top-right corner of the page.

<figure markdown="span">
![Create Project](assets/create-project.jpg){ align=center }
<figcaption>The location of the "Create" button</figcaption>
</figure>

Provide a name and a description of the project that reflects your goals.  In this example, the project will be named "People Detection", which will be used in all future tutorials requiring a user-created project.

<figure markdown="span">
![Project Details](assets/create-project-fields.jpg){ align=center }
<figcaption>Project Details</figcaption>
</figure>

Your newly created project will be placed next to the public project named "Sample Datasets". This public project contains public datasets for users to become familiar with how datasets are managed in EdgeFirst Studio. 

!!! Warning
    The "Sample Datasets" project is **READ ONLY**.  Significant Studios functionality will need write-access to a project and will fail when attempted to be run on this project!

<figure markdown="span">
![New Project](assets/new-project.jpg){ align=center }
<figcaption>Both Projects</figcaption>
</figure>

In this Quickstart guide, you have created your EdgeFirst Studio Account, logged in to EdgeFirst Studio, and created your very first project. The following links will provide additional tutorials for user onboarding in EdgeFirst Studio.

* [EdgeFirst Studio: From Start to Deployment](getting_started/workflows.md)
* [Navigating EdgeFirst Studio](getting_started/studio.md)
* [Dataset Management](getting_started/datasets.md)
* [Model Training, Validation, and Deployment](getting_started/models.md)
* [Command-Line Interface: Using the EdgeFirst Studio Middleware](getting_started/perception.md)
* [EdgeFirst Platforms: Setup and Boot Guide](getting_started/platforms.md)

[signup]: #
[login]: #