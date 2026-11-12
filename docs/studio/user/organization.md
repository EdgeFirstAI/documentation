# Organization Management

When you first [sign up](profile.md#sign-up) to EdgeFirst Studio, you will also automatically create your own organization.  For multi-user tiers, an organization allows multiple users to access your projects, but at the start, you will be the only user in your organization.  However, you can [create multiple users/profiles](#add-new-users) in your organization to allow collaboration between members in your team.  In this way, multiple members can be assigned to your organization.

You can find the information of your organization by clicking on the "User" button that is found on the top right of the navigation bar as shown below.  You will see three different options, click on the "Admin Console" button.

{{ figure("../assets/user/admin-button.jpg", "User Button") }}

This will navigate you to the "Organization Information" page.  Shown below is an example.

{{ figure("../assets/user/organization-information.jpg", "Organization Information") }}

## Edit Organization Information

You can edit your organization's information by clicking either the "Edit" button or the "Edit Info" button from the "Organization Information" page as shown below.

{{ figure("../assets/user/edit-organization-information.jpg", "Edit Organization Information") }}

This will bring you to the page that provides input fields to edit the details about your organization.  Add the details of your organization.  Next click "Apply" to save the changes or "Cancel" to abort the changes.  Shown below is an example.

{{ figure("../assets/user/edit-organization-fields.jpg", "Organization Details") }}

## Image Limit

Under "Security", you can set a warning if the number of images in your organization exceeds the limit specified.  The storage of images costs credits and increasing volumes of images will incur more costs.  This feature was added to provide warnings that the amount of images stored has exceeded the limit you've specified.  You can find more information under [Billing Information](billing.md).

You can set the image limit warning as shown below.  Once the value has been set, go ahead and click "Apply" to set the limit.  Otherwise, you can click on "Cancel" to abort changes.

{{ figure("../assets/user/set-image-limit.jpg", "Set Image Limit") }}

In this example, I have set the limit to 50 and since my organization contains more than 50 images, the warning is triggered as shown below.

{{ figure("../assets/user/image-limit-warning.jpg", "Image Limit Warning") }}

## User Management

This section will provide details about the users in your organization.  The following organization rules are applied to any user.

1. A user belongs to one organization.
2. A user cannot change organizations.
3. An admin user creates the accounts for other users in the organization.
4. Any user cannot invite other users in different organizations.

The user who signs up is the admin of the organization.  However, this user can also set other users in the organization as admin or non-admin. The difference between admin and non-admin users is that admin users can add new users or remove users from the organization.

### Current Users

You can see the list of all users in your organization by clicking on "User Manager" as shown below.

{{ figure("../assets/user/user-manager.jpg", "User Manager") }}

As an admin user, you can edit the information of each user by clicking the "pencil" ![Pencil Button](../../assets/buttons/studio-edit-user-button.jpg) button next to their profiles.  This will bring the page that allows you to modify the user's profile information.  From this page you can change the first and last name of the user and their email.  You can also set the user's role as either admin or non-admin. You can either click "Apply" to save the changes or "Cancel" to abort any changes.  Lastly, you can also change the user's password.

{{ figure("../assets/user/modify-user-information.jpg", "Modify User Information") }}

{% include-markdown "discrete/user/new_users.md" heading-offset=2 %}

## Next Steps

This page has shown how to manage your organization and the users in your organization.  For information on how the billing in your organization is handled, see [Billing Information](billing.md).
