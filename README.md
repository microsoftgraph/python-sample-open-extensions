# Working with Graph open extensions in Python

Many resources in Microsoft Graph support _open extensions_: untyped properties that can be attached to a resource instance. This sample shows how to read and write open extensions in Python.

* [Installation](#installation)
* [Running the sample](#running-the-sample)
* [Helper functions](#helper-functions)
* [Contributing](#contributing)
* [Resources](#resources)

## Installation

To install and configure the samples, see the instructions in [Installing the Python REST samples](https://github.com/microsoftgraph/python-sample-auth/blob/master/installation.md). Note that the samples in this repo require **User.Read** and **Directory.AccessAsUser.All** permissions.

After you've completed those steps, you'll be able to run the sample.py sample as covered below.

## Running the sample

1. At the commend prompt: ```python sample.py```
2. In your browser, navigate to [http://localhost:5000](http://localhost:5000)
3. Choose **Log in** and authenticate with a Microsoft identity (work or school account or Microsoft account). For this sample, you'll need to use an admin account because of the requirement for the **Directory.AccessAsUser.All** scope, which requires admin consent.

You'll then see a page where you can select a "color preference" for the current user:

![screenshot](/static/images/screenshot1.png)

Choose one of the color buttons, and you'll see your selection. For example, here we've selected "Green" for a test account:

![screenshot](/static/images/screenshot2.png)

The selected color preference is automatically saved to a ```color``` setting in an open extension named ```graph-python-sample``` under the user's resource instance in Microsoft Graph. You can verify this with Graph Explorer:

1. Navigate a browser to [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer#)
2. Choose **Sign in with Microsoft** and authenticate under the same identity you used while running the sample.
3. To display the sample queries for Extensions, choose **show more samples** and make sure the **Extensions** category is switched **On**.
4. Click on the sample named **get an open extension** and then choose **Run Query**.

You'll then see the open extensions for this user node, which will include the color preference setting that was saved by the sample code:

![Graph Explorer](/static/images/screenshot3.png)

Because this setting is stored with the user's identity in Microsoft Graph, it will "roam" with this user identity across sessions. This is a simple example with a single setting, but the core concepts can be used to manage user preferences for your application to persist them across sessions and provide an intuitive and consistent experience across multiple devices. You can also use these techniques to add custom metadata to other Graph resources such as devices, groups, or organizations.

## Helper functions

Two helper functions are provided in this sample, which you can use to manage open extensions in Python applications.

The ```open_extension_read()``` function reads a named open extension from a Graph resource and returns it as a Python dictionary. For example, here's how the sample app reads the user's color preference setting:

```python
settings = open_extension_read(client=MSGRAPH, ext_name=EXTENSION_NAME)
selected_color = settings.get('color', '')
```

The ```open_extension_write()``` function writes a Python dictionary of settings as an open extension. For example, here's the code that saves the user's color preference selection in the sample app:

```python
response = open_extension_write(client=MSGRAPH,
                                ext_name=EXTENSION_NAME,
                                settings={'color': selected_color})
```

The helper functions take an optional ```entity``` argument to specify the type of entity the extensions are stored on. The sample app uses the default 'me' entity, but Graph supports open extensions on many other nodes as well, including devices, calendar events, mail messages, and others.

Here's a summary of the types of open extensions that are currently supported:

| Supported Resource | Endpoint (entity argument) | Permission Required |
| ------------------ | -------------------------- | ------------------- |
| device | devices/{id} | Device.ReadWrite.All |
| event | users/{id|userPrincipalName}/events/{id} | Calendars.ReadWrite |
| group | groups/{id} | Group.ReadWrite.All |
| group event | groups/{id}/events/{id} | Group.ReadWrite.All |
| group post | groups/{id}/threads/{id}/posts/{id} | Group.ReadWrite.All |
| message | users/{id or userPrincipalName}/messages/{id} | Mail.ReadWrite |
| organization | organization/{id} | Directory.AccessAsUser.All |
| personal contact | users/{id or userPrincipalName}/contacts/{id} | Contacts.ReadWrite |
| user | 'me' or 'users/{id or userPrincipalName}' | Directory.AccessAsUser.All |

For more information about creating other types of open extensions, see [Create open extension](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/opentypeextension_post_opentypeextension).

## Contributing

These samples are open source, released under the [MIT License](https://github.com/microsoftgraph/python-sample-pagination/blob/master/LICENSE). Issues (including feature requests and/or questions about this sample) and [pull requests](https://github.com/microsoftgraph/python-sample-pagination/pulls) are welcome. If there's another Python sample you'd like to see for Microsoft Graph, we're interested in that feedback as well &mdash; please log an [issue](https://github.com/microsoftgraph/python-sample-pagination/issues) and let us know!

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Resources

Documentation:
* [openTypeExtension resource type (open extensions)](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/resources/opentypeextension)
* [Add custom data to users using open extensions](https://developer.microsoft.com/en-us/graph/docs/concepts/extensibility_open_users)
* [Create open extension](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/opentypeextension_post_opentypeextension)
* [Get open extension](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/opentypeextension_get)

Samples:
* [Python authentication samples for Microsoft Graph](https://github.com/microsoftgraph/python-sample-auth)
* [Sending mail via Microsoft Graph from Python](https://github.com/microsoftgraph/python-sample-send-mail)
* [Working with paginated Microsoft Graph responses in Python](https://github.com/microsoftgraph/python-sample-pagination)
* [Working with Graph open extensions in Python](https://github.com/microsoftgraph/python-sample-open-extensions)
