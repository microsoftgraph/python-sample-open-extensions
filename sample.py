"""graphrest sample for Microsoft Graph"""
# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
import json
import os

import bottle
import graphrest

EXTENSION_NAME = 'graph-python-sample'

MSGRAPH = graphrest.GraphSession()

bottle.TEMPLATE_PATH = ['./static/templates']

@bottle.route('/')
@bottle.view('homepage.html')
def homepage():
    """Render the home page."""

    # If a postback, the 'color' parameter contains the selected color.
    selected_color = bottle.request.query.color

    if MSGRAPH.state['loggedin']:
        # user has logged in
        user_data = MSGRAPH.get('me').json()
        user_identity = user_data['userPrincipalName']
        if selected_color:
            # user selected a color preference, so save it
            response = open_extension_write(client=MSGRAPH,
                                            ext_name=EXTENSION_NAME,
                                            settings={'color': selected_color})
            if not response.ok:
                print(f'ERROR SAVING EXTENSION: {response}')
        else:
            # read user's color preference from their saved settings
            settings = open_extension_read(client=MSGRAPH,
                                           ext_name=EXTENSION_NAME)
            selected_color = settings.get('color', '')
    else:
        # anonymous, no user logged in
        user_identity = None
        selected_color = 'white'

    return {'user_identity': user_identity, 'color': selected_color}

@bottle.route('/login')
def login():
    """Prompt user to authenticate."""
    MSGRAPH.login('/')

@bottle.route('/logout')
def logout():
    """Log out."""
    MSGRAPH.logout('/')

@bottle.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect URI."""
    MSGRAPH.redirect_uri_handler()

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    """Handler for static files, used with the development server."""
    root_folder = os.path.abspath(os.path.dirname(__file__))
    return bottle.static_file(filepath, root=os.path.join(root_folder, 'static'))

def open_extension_read(client, *, ext_name, entity='me'):
    """Read an open extension from a Graph resource instance.

    client   = Graph connection object supporting .get(), .post(), .patch()
    entity   = the type of resource that this extension data is associated with.
               Defaults to 'me' for user node extensions, but can be any Graph
               endpoint that allows the /extensions navigation property.
    ext_name = name of the extension (unique identifier)

    Returns a dictionary of the settings for the specified extension name.
    Returns empty dictionary if extension not found.
    """
    jsondata = client.get(entity + '?$select=id&$expand=extensions').json()
    for extension in jsondata.get('extensions'):
        if extension['id'] == ext_name:
            return extension
    return {} # requested extension not found

def open_extension_write(client, *, ext_name, entity='me', settings):
    """Write an open extension to a Graph resource instance.

    client   = Graph connection object supporting .get(), .post(), .patch()
    entity   = the type of resource that this extension data is associated with.
               Defaults to 'me' for user node extensions, but can be any Graph
               endpoint that allows the /extensions navigation property.
    ext_name = name of the extension (unique identifier)
    settings = a dictionary of key/value pairs to be saved

    If the extension already exists, do a PATCH to replace existing settings.
    If the extension does not exist, do a POST to create it.
    Returns the response from the PATCH OR POST.
    """

    extension_data = {'@odata.type': 'Microsoft.Graph.OpenTypeExtension',
                      'extensionName': ext_name,
                      'id': ext_name}
    extension_data.update(settings)
    request_data = json.dumps(extension_data)

    if open_extension_read(client, ext_name=EXTENSION_NAME):
        # extension exists, so PATCH to update its color setting
        return client.patch(entity + '/extensions/' + ext_name, data=request_data)

    # extension doesn't exist, so POST to create it
    return client.post(entity + '/extensions', data=request_data)

if __name__ == '__main__':
    bottle.run(app=bottle.app(), server='wsgiref', host='localhost', port=5000)
