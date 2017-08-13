import os
from time import time

from fixtures import Fixture

from egnyte_client import EgnyteClient


class UserFixture(Fixture):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username', 'testuser{}'.format(time()))
        self.email = kwargs.get('email', '{}@exampl.net'.format(self.username))
        self.external_id = kwargs.get('external_id', '236318678')
        self.family_name = kwargs.get('family_name', 'john')
        self.given_name = kwargs.get('given_name', 'doe')
        self.active = kwargs.get('active', True)
        self.send_invite = kwargs.get('send_invite', False)
        self.auth_type = kwargs.get('auth_type', 'egnyte')
        self.user_type = kwargs.get('user_type', 'standard')

    def _setUp(self):
        client = EgnyteClient()

        new_user = client.create_user(
            username=self.username,
            email=self.email,
            external_id=self.external_id,
            family_name=self.family_name,
            given_name=self.given_name,
            active=self.active,
            send_invite=self.send_invite,
            auth_type=self.auth_type,
            user_type=self.user_type
        )
        self.user_id = new_user['id']

        self.addCleanup(client.delete_user, new_user['id'])


class FolderFixture(Fixture):
    def __init__(self, **kwargs):
        self.folder_name = kwargs.get('folder_name', 'folder5678'.format(time()))
        self.parent_folder = kwargs.get(
            'parent_folder',
            os.getenv('EGNYTE_TEST_DIR', 'Shared/__Maria')
        )

        self.full_path = '{}/{}'.format(self.parent_folder, self.folder_name)

    def _setUp(self):
        client = EgnyteClient()

        client.create_folder(self.full_path)
        self.addCleanup(
            client.remove_file_or_folder,
            self.full_path,
            ignore_not_found=True
        )
        # client.remove_file_or_folder is a link for a function,
        # remove_file_or_folder() calls for  a function immediately instead

