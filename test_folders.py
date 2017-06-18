import unittest
import tempfile
from egnyte_client import EgnyteClient
from base64 import b64decode



class TestFilesAndFoldersListing(unittest.TestCase):
    def setUp(self):
        super(TestFilesAndFoldersListing, self).setUp()

        self.client = EgnyteClient()

    def test_file_exists_in_listing(self):
        pass

    def test_folder_exists_in_listing(self):
        folder_to_list = 'Shared'
        expected_to_find = 'ThisFolderIWantToFind'
        folder_path = '{}/{}'.format(folder_to_list, expected_to_find)

        self.client.create_folder(folder_path)
        self.addCleanup(self.client.remove_file_or_folder, folder_path, True)

        listing = self.client.get_listing(folder_to_list)
        folder_names_in_listing = []
        for f in listing['folders']:
            folder_names_in_listing.append(f['name'])

        self.assertIn(expected_to_find, folder_names_in_listing)

    def test_folder_created(self):
        folder_to_create = 'TheBestFolderInTheWorld'
        parent_folder = 'Shared'
        folder_path = '{}/{}'.format(parent_folder, folder_to_create)

        self.client.create_folder(folder_path)
        self.addCleanup(self.client.remove_file_or_folder, folder_path, True)

        folder_listing = self.client.get_listing(parent_folder)

        folder_names_in_listing = [f['name']
                                   for f in folder_listing['folders']]
        self.assertIn(folder_to_create, folder_names_in_listing)

    def test_rename_folder(self):
        parent_folder = 'Shared'
        old_folder_name = 'FolderIsNotYetRenamed'
        new_folder_name = 'FolderHasBeenRenamed'
        folder_path_before_rename = '{}/{}'.format(parent_folder,
                                                   old_folder_name)
        folder_path_after_rename = '/{}/{}'.format(parent_folder,
                                                   new_folder_name)

        self.client.create_folder(folder_path_before_rename)
        self.addCleanup(
            self.client.remove_file_or_folder,
            folder_path_before_rename,
            True
        )

        self.client.rename_folder(
            folder_path_before_rename,
            folder_path_after_rename
        )

        self.addCleanup(
            self.client.remove_file_or_folder,
            folder_path_after_rename,
            True
        )

        folder_listing = self.client.get_listing(parent_folder)

        folder_names_in_listing = [f['name']
                                   for f in folder_listing['folders']]
        self.assertIn(new_folder_name, folder_names_in_listing)

    def test_remove_folder(self):
        parent_folder = 'Shared'
        new_folder = 'BrandNewFolder'
        folder_path = '{}/{}'.format(parent_folder, new_folder)

        self.client.create_folder(folder_path)
        self.client.remove_file_or_folder(folder_path)

        folder_listing = self.client.get_listing(parent_folder)

        folder_names_in_listing = []

        for f in folder_listing['folders']:
            folder_names_in_listing.append(f['name'])

        self.assertNotIn(new_folder, folder_names_in_listing)

    def test_upload_file(self):
        parent_folder = 'Shared/__Maria'
        file_name = 'TestUploadFile.txt'
        full_path = '{}/{}'.format(parent_folder, file_name)

        with tempfile.TemporaryFile() as fp:
            fp.write(b'Hello World!\n')
            fp.seek(0)

            self.client.upload_file(fp, full_path)
            self.addCleanup(self.client.remove_file_or_folder, full_path, True)

    def test_file_is_restored_from_trash(self):
        parent_folder = 'Shared/__Maria'
        file_name_to_list = 'FileToRestoreFromTrash.txt'
        full_path = '{}/{}'.format(parent_folder, file_name_to_list)

        with tempfile.TemporaryFile() as fp:
            fp.write(b'Hello World!\n')
            fp.seek(0)

            uploaded_file_response = self.client.upload_file(fp, full_path)
            self.client.remove_file_or_folder(full_path)

            trash_listing = self.client.get_listing('trash')
            file_in_trash = None

            for f in trash_listing['items']:
                encoded_id_of_file = f['id']
                decoded_id_of_file = b64decode(encoded_id_of_file)
                decoded_id_of_file = decoded_id_of_file.decode("utf-8")

                group_id, _, __ = decoded_id_of_file.split('|')

                if group_id == uploaded_file_response['group_id']:
                    file_in_trash = f
                    break

            self.assertIsNotNone(file_in_trash, 'File was not found in trash')
            # TODO: Restore the file from trash and check it's back in folder