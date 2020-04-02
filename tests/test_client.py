# #!/usr/bin/env python

import json
import unittest

import googleapiclient.http
import googleapiclient.discovery

import googlesheets.api
import googlesheets.request

pretty = lambda o: json.dumps(o, indent=1, default=str)

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.ok = {
            'status': '200'
        }

        self.not_found = {
            'status': '404'
        }

        http = googleapiclient.http.HttpMock(
            'data/config-v4/sheets-discovery.json',
            self.ok)

        self.client = googlesheets.api.Client('')

        self.client.service = googleapiclient.discovery.build(
            'sheets',
            'v4',
            http=http,
            developerKey='secret').spreadsheets()

    def test_batch_get_all_rows(self):
        req = googlesheets.request.BatchGetValuesFormatted()
        req.append(f'sheets!A1')

        http = googleapiclient.http.HttpMock('data/response-v4/batch-values-get.json', self.ok)
        res = self.client.batch_values_get(req, transport=http)

        print(
            pretty(res))

    def test_batch_get_all_rows_no_headers(self):
        req = googlesheets.request.BatchGetValuesFormatted()
        req.append(f'sheets!A1')

        http = googleapiclient.http.HttpMock('data/response-v4/batch-values-get.no-header.json', self.ok)
        res = self.client.batch_values_get(req, transport=http)

        print(
            pretty(res))

# from googleapiclient.errors import HttpError
#     try:
#         res = googlesheets_client.get_spreadsheet('xxxyyyzzz')
#     except HttpError as err:
#         print(f'got error:\n{err}')
#         if err.resp.get('content-type', '').startswith('application/json'):
#             reason = json.loads(err.content)
#             print(reason)
#             print(reason['error']['code'])
#             print(reason['error']['message'])
#         print(f'error code: {err.resp.status}')
#         print(f'error res: {err.resp}')
#     except Exception as err:
#         print(f'could not catch error:\n{err}')
