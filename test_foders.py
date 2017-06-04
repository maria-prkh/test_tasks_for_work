import json
import unittest

import requests


class EgnyteClient(object):
    host_name = 'newparity.qa-egnyte.com'
    token = 'bjy9hd796yx7gxpeju5tq59t'

    def get_url(self, folder_path):
        """Gets url for a concrete folder."""
        url_tpl = 'https://{host}/pubapi/v1/fs/{folder}'
        return url_tpl.format(host=self.host_name, folder=folder_path)

    def get_listing(self, folder_name):
        """To get json with list of folders which contains specified folder."""
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }
        url = self.get_url(folder_name)
        resp = requests.get(url, headers=headers)

        resp.raise_for_status()

        return resp.json()

    def create_folder(self, folder_path):
        """Creates folder for a specified folder path."""

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }

        data = {"action": "add_folder"}
        url = self.get_url(folder_path)

        resp = requests.post(url, data=json.dumps(data), headers=headers)
        resp.raise_for_status()

    def remove_folder(self, folder_path, ignore_not_found=False):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }

        url = self.get_url(folder_path)

        resp = requests.delete(url, headers=headers)

        if resp.status_code == 404 and ignore_not_found:
            return

        resp.raise_for_status()

    def upload_file(self, folder_path, file_path):
        """Uploads a file to the specified folder path."""
        pass

    def rename_folder(self, original_path, destination_path):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }

        data = {
            "action": "move",
            "destination": destination_path
        }

        url = self.get_url(original_path)
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()


class TestFilesAndFoldersListing(unittest.TestCase):
    def setUp(self):
        super(TestFilesAndFoldersListing, self).setUp()

        self.client = EgnyteClient()

    def test_file_exists_in_listing(self):
        pass

    def test_folder_exists_in_listing(self):
        folder_to_list = 'Shared'
        expected_to_find = 'adghfdghhg'
        folder_path = '{}/{}'.format(folder_to_list, expected_to_find)

        self.client.create_folder(folder_path)
        self.addCleanup(self.client.remove_folder, folder_path, True)

        listing = self.client.get_listing(folder_to_list)
        folder_names_in_listing = [f['name'] for f in listing['folders']]

        self.assertIn(expected_to_find, folder_names_in_listing)

    def test_folder_created(self):
        folder_to_create = 'ssdkoooljj'
        parent_folder = 'Shared'
        folder_path = '{}/{}'.format(parent_folder, folder_to_create)

        self.client.create_folder(folder_path)
        self.addCleanup(self.client.remove_folder, folder_path, True)

        folder_listing = self.client.get_listing(parent_folder)

        folder_names_in_listing = [f['name'] for f in folder_listing['folders']]
        self.assertIn(folder_to_create, folder_names_in_listing)

    def test_rename_folder(self):
        parent_folder = 'Shared'
        old_folder_name = 'FolderIsNotYetRenamed'
        new_folder_name = 'FolderHasBeenRenamed'
        folder_path_before_rename = '{}/{}'.format(parent_folder, old_folder_name)
        folder_path_after_rename = '/{}/{}'.format(parent_folder, new_folder_name)

        self.client.create_folder(folder_path_before_rename)
        self.addCleanup(self.client.remove_folder, folder_path_before_rename, True)

        self.client.rename_folder(folder_path_before_rename, folder_path_after_rename)
        self.addCleanup(self.client.remove_folder, folder_path_after_rename, True)

        folder_listing = self.client.get_listing(parent_folder)

        folder_names_in_listing = [f['name'] for f in folder_listing['folders']]
        self.assertIn(new_folder_name, folder_names_in_listing)

    def test_remove_folder(self):
        parent_folder = 'Shared'
        new_folder = 'dakjda'
        folder_path = '{}/{}'.format(parent_folder, new_folder)

        self.client.create_folder(folder_path)
        self.client.remove_folder(folder_path)

        folder_listing = self.client.get_listing(parent_folder)

        folder_names_in_listing = [f['name'] for f in
                                   folder_listing['folders']]
        self.assertNotIn(new_folder, folder_names_in_listing)




