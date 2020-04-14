# #!/usr/bin/env python

import pathlib
import unittest

import googleapiclient.http
import googleapiclient.errors
import googleapiclient.discovery

import googlesheets.api
import googlesheets.resource

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.ok = {
            'status': '200'
        }

        self.not_found = {
            'status': '404'
        }

        self.invalid_arg = {
            'status': '400',
            'content-type': 'application/json',
            'error': {
                'error_details': {
                    'vary': 'Origin, X-Origin, Referer',
                    'content-type': 'application/json; charset=UTF-8',
                    'transfer-encoding': 'chunked',
                    'status': '400',
                    'content-length': '122',
                    '-content-encoding': 'gzip'
                }
            }
        }

        self.cwd = pathlib.Path(__file__).parent

        http = googleapiclient.http.HttpMock(
            self.cwd / 'data/config-v4/sheets-discovery.json',
            self.ok)

        self.client = googlesheets.api.Client('')

        self.client.service = googleapiclient.discovery.build(
            'sheets',
            'v4',
            http=http,
            developerKey='secret').spreadsheets()

    def test_get_spreadsheet(self):
        http = googleapiclient.http.HttpMock(self.cwd / 'data/response-v4/get-spreadsheet.json', self.ok)
        res = self.client.get_spreadsheet(refresh=True, transport=http)

        self.assertIsNotNone(res)

    def test_batch_get_all_rows(self):
        req = googlesheets.resource.ValuesBatchGetFormatted()
        req.append(f'sheets!A1')

        http = googleapiclient.http.HttpMock(self.cwd / 'data/response-v4/batch-values-get.json', self.ok)
        res = self.client.batch_values_get(req, transport=http)

        self.assertIsNotNone(res)

    def test_batch_get_all_rows_no_headers(self):
        req = googlesheets.resource.ValuesBatchGetFormatted()
        req.append(f'sheets!A1')

        http = googleapiclient.http.HttpMock(self.cwd / 'data/response-v4/batch-values-get.no-header.json', self.ok)

        res = self.client.batch_values_get(req, transport=http)

        self.assertIsNotNone(res)

    def test_error_handling(self):
        req = googlesheets.resource.ValuesBatchGetFormatted()
        req.append(f'sheets!A1')

        http = googleapiclient.http.HttpMock(self.cwd / 'data/response-v4/batch-values-get-invalid-argument.json', self.invalid_arg)

        try:
            self.client.batch_values_get(req, transport=http)
        except googleapiclient.errors.HttpError as e:
            reason = googlesheets.api.parse_http_error(e)

            self.assertIsNotNone(reason)
            self.assertEqual(reason['error']['code'], 400)
            self.assertEqual(reason['error']['message'], 'Unable to parse range: sheets.xA1')
