#!/usr/bin/env python

# pylint: disable=fixme

import pathlib

import googleapiclient.discovery
import google.oauth2.service_account

import googlesheets.request


class Client(object):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

    def __init__(self, spreadsheet_id: str) -> None:
        self.json_keyfile = None
        self.service = None

        self.cached_spreadsheet = None # cached spreadsheet object

        self.spreadsheet_id = spreadsheet_id

    def init(self, json_keyfile: pathlib.Path, version: str = 'v4') -> None:
        """instantiate the service client and complete authorization via oauth2 flow."""

        credentials = google.oauth2.service_account.Credentials.from_service_account_file(str(json_keyfile), scopes=Client.SCOPES)

        params = {
            'credentials': credentials,
            'discoveryServiceUrl': Client.DISCOVERY_URL,
        }

        self.service = googleapiclient.discovery.build('sheets', version, **params).spreadsheets()

    def spreadsheet(self, refresh: bool = True) -> dict:
        """submit a request for the current spreadsheet. if `refresh` is `False`, returns a cached value."""

        params = {
            'spreadsheetId': self.spreadsheet_id
        }

        req = self.service.get(**params)

        try:
            res = req.execute()
        except Exception:
            raise
        else:
            if self.cached_spreadsheet is None or refresh:
                self.cached_spreadsheet = res

            return self.cached_spreadsheet

    def batch_update(self, payload: googlesheets.request.RequestBody) -> dict:
        """submit a batch update request. note: update differs from values.update."""

        params = {
            'spreadsheetId': self.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.batchUpdate(**params)

        try:
            return req.execute()
        except Exception:
            raise

    def batch_values_get(self, payload: googlesheets.request.RequestBody) -> dict:
        """submit a batch values get request."""

        if 'valueRenderOption' not in payload.body:
            raise ValueError('missing required field: "valueRenderOption"')

        params = {
            'spreadsheetId': self.spreadsheet_id,
            'ranges': payload.body.get('ranges'),
            'valueRenderOption': payload.body.get('valueRenderOption')
        }

        if 'dateTimeRenderOption' in payload.body:
            params['dateTimeRenderOption'] = payload.body['dateTimeRenderOption']

        req = self.service.values().batchGet(**params)

        try:
            return req.execute()
        except Exception:
            raise

    def batch_values_update(self, payload: googlesheets.request.RequestBody) -> dict:
        """submit a batch values update request. note: values.update differs from update."""

        params = {
            'spreadsheetId': self.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.values().batchUpdate(**params)

        try:
            return req.execute()
        except Exception:
            raise

    def batch_values_clear(self, payload: googlesheets.request.RequestBody) -> dict:
        """submit a batch values clear request."""

        params = {
            'spreadsheetId': self.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.values().batchClear(**params)

        try:
            return req.execute()
        except Exception:
            raise
