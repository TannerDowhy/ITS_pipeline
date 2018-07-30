#!/usr/bin/env python

"""Sync a directory between two Globus endpoints. Defaults:
Source: Globus Tutorial Endpoint 1: /share/godata
Destination: Globus Tutorial Endpoint 2: /~/sync-demo/
# Checkout the Destination at:
globus.org/app/transfer?destination_id=ddb59af0-6d04-11e5-ba46-22000b92c6ec
Authorization only needs to happen once, afterwards tokens are saved to disk
(MUST BE STORED IN A SECURE LOCATION). Store data is already checked for
previous transfers, so if this script is run twice in quick succession,
the second run won't queue a duplicate transfer."""

import json
import sys
import webbrowser
import os
import six

from globus_sdk import (NativeAppAuthClient, TransferClient,
                        RefreshTokenAuthorizer, TransferData)
from globus_sdk.exc import GlobusAPIError, TransferAPIError

# Globus Tutorial Endpoint 1
SOURCE_ENDPOINT = 'bb48aa3e-67fe-11e7-a9a4-22000bf2d287'
# Globus Tutorial Endpoint 2
DESTINATION_ENDPOINT = 'c99fd40c-5545-11e7-beb6-22000b9a448b'
# Copy data off of the endpoint share
SOURCE_PATH = '/datastore/P2IRC13/Data/DNA_sequencing/fastq_files/Canola_2016/Sample_names_corrected/'

# Destination Path -- The directory will be created if it doesn't exist
DESTINATION_PATH = '/~/scratch/test'

TRANSFER_LABEL = 'Folder Sync Example'

# You will need to register a *Native App* at https://developers.globus.org/
# Your app should include the following:
#     - The scopes should match the SCOPES variable below
#     - Your app's clientid should match the CLIENT_ID var below
#     - "Native App" should be checked
# For more information:
# https://docs.globus.org/api/auth/developer-guide/#register-app
CLIENT_ID = '19ca51f3-41fd-4cd6-90c2-61118d0bafa2'
CLIENT_SECRET = '2CpOhEQfcAK3GQmYtjtCUgZt+mHevJhQ6Nr08fmPNn4='
DATA_FILE = 'transfer-data.json'
REDIRECT_URI = 'https://auth.globus.org/v2/oauth2/authorize'
# SCOPES = ('openid email profile '
#           'urn:globus:auth:scope:frdr-dev6.computecanada.ca:all urn:globus:auth:scope:frdr-dev5.computecanada.ca:all')
# REDIRECT_URI = ('https://auth.globus.org/v2/oauth2/authorize?client_id=19ca51f3-41fd-4cd6-90c2-61118d0bafa2')

# ONLY run new tasks if there was a previous task and it exited with one of the
# following statuses. This is ignored if there was no previous task.
# The previous task is queried from the DATA_FILE
PREVIOUS_TASK_RUN_CASES = ['SUCCEEDED', 'FAILED']

# Create the destination folder if it does not already exist
CREATE_DESTINATION_FOLDER = True


get_input = getattr(__builtins__, 'raw_input', input)


def do_native_app_authentication(client_id, redirect_uri,
                                 requested_scopes=None):
    """
    Does a Native App authentication flow and returns a
    dict of tokens keyed by service name.
    """
    client = NativeAppAuthClient(client_id=client_id)
    # pass refresh_tokens=True to request refresh tokens
    client.oauth2_start_flow(requested_scopes=requested_scopes,
                             redirect_uri=redirect_uri,
                             refresh_tokens=True)

    url = client.oauth2_get_authorize_url()

    print('Native App Authorization URL:\n{}'.format(url))

    if not is_remote_session():
        # There was a bug in webbrowser recently that this fixes:
        # https://bugs.python.org/issue30392
        # if sys.platform == 'darwin':
        #     webbrowser.get('safari').open(url, new=1)
        # else:
        webbrowser.open(url, new=1)

    auth_code = get_input('Enter the auth code: ').strip()

    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    # return a set of tokens, organized by resource server name
    return token_response.by_resource_server


def load_data_from_file(filepath):
    """Load a set of saved tokens."""
    with open(filepath, 'r') as f:
        tokens = json.load(f)

    return tokens


def save_data_to_file(filepath, key, data):
    """Save data to a file"""
    try:
        store = load_data_from_file(filepath)
    except:
        store = {}
    store[key] = data
    with open(filepath, 'w') as f:
        json.dump(store, f)


def update_tokens_file_on_refresh(token_response):
    """
    Callback function passed into the RefreshTokenAuthorizer.
    Will be invoked any time a new access token is fetched.
    """
    save_data_to_file(DATA_FILE, 'tokens', token_response.by_resource_server)


def get_tokens():
    tokens = None
    try:
        # if we already have tokens, load and use them
        tokens = load_data_from_file(DATA_FILE)['tokens']
    except:
        pass

    if not tokens:
        # if we need to get tokens, start the Native App authentication process
        tokens = do_native_app_authentication(CLIENT_ID, REDIRECT_URI, SCOPES)

        try:
            save_data_to_file(DATA_FILE, 'tokens', tokens)
        except:
            pass

    return tokens


def is_remote_session():
    return os.environ.get('SSH_TTY', os.environ.get('SSH_CONNECTION'))


def setup_transfer_client(transfer_tokens):

    authorizer = RefreshTokenAuthorizer(
        transfer_tokens['refresh_token'],
        NativeAppAuthClient(client_id=CLIENT_ID),
        access_token=transfer_tokens['access_token'],
        expires_at=transfer_tokens['expires_at_seconds'],
        on_refresh=update_tokens_file_on_refresh)

    transfer_client = TransferClient(authorizer=authorizer)

    try:
        transfer_client.endpoint_autoactivate(SOURCE_ENDPOINT)
        transfer_client.endpoint_autoactivate(DESTINATION_ENDPOINT)
    except GlobusAPIError as ex:
        if ex.http_status == 401:
            sys.exit('Refresh token has expired. '
                     'Please delete the `tokens` object from '
                     '{} and try again.'.format(DATA_FILE))
        else:
            raise ex
    return transfer_client


def check_endpoint_path(transfer_client, endpoint, path):
    """Check the endpoint path exists"""
    try:
        transfer_client.operation_ls(endpoint, path=path)
    except TransferAPIError as tapie:
        print('Failed to query endpoint "{}": {}'.format(
            endpoint,
            tapie.message
        ))
        sys.exit(1)


def create_destination_directory(transfer_client, dest_ep, dest_path):
    """Create the destination path if it does not exist"""
    try:
        transfer_client.operation_ls(dest_ep, path=dest_path)
    except TransferAPIError:
        try:
            transfer_client.operation_mkdir(dest_ep, dest_path)
            print('Created directory: {}'.format(dest_path))
        except TransferAPIError as tapie:
            print('Failed to start transfer: {}'.format(tapie.message))
            sys.exit(1)


def main():

    tokens = get_tokens()
    transfer = setup_transfer_client(tokens['transfer.api.globus.org'])

    try:
        task_data = load_data_from_file(DATA_FILE)['task']
        task = transfer.get_task(task_data['task_id'])
        if task['status'] not in PREVIOUS_TASK_RUN_CASES:
            print('The last transfer status is {}, skipping run...'.format(
                task['status']
            ))
            sys.exit(1)
    except KeyError:
        # Ignore if there is no previous task
        pass

    check_endpoint_path(transfer, SOURCE_ENDPOINT, SOURCE_PATH)
    if CREATE_DESTINATION_FOLDER:
        create_destination_directory(transfer, DESTINATION_ENDPOINT,
                                     DESTINATION_PATH)
    else:
        check_endpoint_path(transfer, DESTINATION_ENDPOINT, DESTINATION_PATH)

    tdata = TransferData(
        transfer,
        SOURCE_ENDPOINT,
        DESTINATION_ENDPOINT,
        label=TRANSFER_LABEL,
        sync_level="checksum"
    )
    tdata.add_item(SOURCE_PATH, DESTINATION_PATH, recursive=True)

    task = transfer.submit_transfer(tdata)
    save_data_to_file(DATA_FILE, 'task', task.data)
    print('Transfer has been started from\n  {}:{}\nto\n  {}:{}'.format(
        SOURCE_ENDPOINT,
        SOURCE_PATH,
        DESTINATION_ENDPOINT,
        DESTINATION_PATH
    ))
    url_string = 'https://globus.org/app/transfer?' + \
        six.moves.urllib.parse.urlencode({
            'origin_id': SOURCE_ENDPOINT,
            'origin_path': SOURCE_PATH,
            'destination_id': DESTINATION_ENDPOINT,
            'destination_path': DESTINATION_PATH
        })
    print('Visit the link below to see the changes:\n{}'.format(url_string))


if __name__ == '__main__':
    main()
