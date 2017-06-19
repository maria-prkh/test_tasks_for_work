import requests
import json

API_TYPE_FS = 'fs'
API_TYPE_FS_CONTENT = 'fs-content'


class EgnyteClient(object):
    host_name = 'newparity.qa-egnyte.com'
    token = 'bjy9hd796yx7gxpeju5tq59t'

    def get_url(self, full_path, api_type):
        """Gets url for a concrete folder."""
        supported_api_types = ('fs', 'fs-content')
        if api_type not in supported_api_types:
            raise ValueError('{} API type is not supported'.format(api_type))

        url_tpl = 'https://{host}/pubapi/v1/{api_type}/{full_path}'
        return url_tpl.format(
            host=self.host_name,
            full_path=full_path,
            api_type=api_type
        )

    def get_listing(self, folder_name):
        """To get json with list of folders which contains specified folder."""

        headers = self.get_headers()
        url = self.get_url(folder_name, API_TYPE_FS)
        resp = requests.get(url, headers=headers)

        resp.raise_for_status()

        return resp.json()

    def create_folder(self, folder_path):
        """Creates folder for a specified folder path."""

        headers = self.get_headers()

        data = {"action": "add_folder"}
        url = self.get_url(folder_path, API_TYPE_FS)

        resp = requests.post(url, data=json.dumps(data), headers=headers)
        resp.raise_for_status()

    def remove_file_or_folder(self, full_path, ignore_not_found=False):
        headers = self.get_headers()

        url = self.get_url(full_path, API_TYPE_FS)

        resp = requests.delete(url, headers=headers)

        if resp.status_code == 404 and ignore_not_found:
            return

        resp.raise_for_status()

    def get_headers(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }
        return headers

    def upload_file(self, fp, file_path):
        """Uploads a file to the specified folder path."""
        headers = self.get_headers()
        url = self.get_url(file_path, API_TYPE_FS_CONTENT)

        resp = requests.post(url, headers=headers, files={'file': fp})

        resp.raise_for_status()

        return resp.json()

    def rename_folder(self, original_path, destination_path):
        headers = self.get_headers()

        data = {
            "action": "move",
            "destination": destination_path
        }

        url = self.get_url(original_path, API_TYPE_FS)
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()

    def restore_file_from_trash(self, *ids):
        headers = self.get_headers()

        body = {
            "action": "RESTORE",
            "ids": list(ids)
        }

        url = self.get_url('trash', API_TYPE_FS)

        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.raise_for_status()


