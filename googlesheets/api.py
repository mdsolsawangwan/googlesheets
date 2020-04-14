#!/usr/bin/env python

import json
import pathlib

import googleapiclient.errors
import googleapiclient.discovery

import google.oauth2.service_account

import googlesheets.resource

def parse_http_error(e: googleapiclient.errors.HttpError) -> dict:
    """helper function for extracting an error object from an http exception."""

    return (
        json.loads(e.content)
        if e.resp.get('content-type', '').startswith('application/json') else
        {}
    )

class Client(object):
    DEFAULT_SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
    ]

    def __init__(self, spreadsheet_id: str) -> None:
        self.spreadsheet_id = spreadsheet_id

        self.service = None
        self.cached_spreadsheet = None # cached spreadsheet object

    def __call__(self, req: 'service.request', transport: 'httplib2.Http' = None) -> dict:
        """executes a request against the googlesheets service api."""

        params = {}

        if transport:
            params['http'] = transport

        try:
            return req.execute(**params)
        except Exception:
            raise

    def init(self, json_keyfile: pathlib.Path, version: str = 'v4') -> None:
        """instantiate the googlesheets oauth2 service client."""

        credentials = google.oauth2.service_account.Credentials.from_service_account_file(
            str(json_keyfile), scopes=Client.DEFAULT_SCOPES)

        params = {
            'credentials': credentials,
            'discoveryServiceUrl': f'https://sheets.googleapis.com/$discovery/rest?version={version}',
        }

        self.service = googleapiclient.discovery.build(
            'sheets', version, **params).spreadsheets()

    def get_spreadsheet(self, refresh: bool = True, transport: 'httplib2.Http' = None) -> dict:
        """submit a request for the current spreadsheet. if `refresh` is `False`, returns a cached value."""

        params = {
            'spreadsheetId': self.spreadsheet_id
        }

        req = self.service.get(**params)

        try:
            res = self(req, transport=transport)
        except Exception:
            raise
        else:
            if self.cached_spreadsheet is None or refresh:
                self.cached_spreadsheet = res

            return self.cached_spreadsheet

    def get(self, transport: 'httplib2.Http' = None) -> dict:
        """submit a get request."""

        params = {
            'spreadsheetId': self.spreadsheet_id
        }

        req = self.service.get(**params)

        return self(req, transport=transport)

    def values_get(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a values get request."""


        if 'valueRenderOption' not in payload.body:
            raise ValueError('missing required field: "valueRenderOption"')

        params = {
            'spreadsheetId': self.spreadsheet_id,
            **payload.body,
        }

        req = self.service.values().get(**params)

        return self(req, transport=transport)

    def values_update(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a values update request."""


        if 'valueInputOption' not in payload.body:
            raise ValueError('missing required field: "valueInputOption"')

        params = {
            'spreadsheetId': self.spreadsheet_id,
            **payload.body,
        }

        req = self.service.values().update(**params)

        return self(req, transport=transport)

    def values_append(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a values append request."""


        if 'valueInputOption' not in payload.body:
            raise ValueError('missing required field: "valueInputOption"')

        params = {
            'spreadsheetId': self.spreadsheet_id,
            **payload.body,
        }

        req = self.service.values().append(**params)

        return self(req, transport=transport)

    def values_clear(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a values clear request."""

        params = {
            'spreadsheetId': self.spreadsheet_id,
            **payload.body,
        }

        req = self.service.values().clear(**params)

        return self(req, transport=transport)

    def batch_update(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a batch update request. note: update differs from values.update."""

        params = {
            'spreadsheetId': self.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.batchUpdate(**params)

        return self(req, transport=transport)

    def batch_values_get(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a batch values get request."""

        if 'valueRenderOption' not in payload.body:
            raise ValueError('missing required field: "valueRenderOption"')

        params = {
            'ranges': payload.body['ranges'],
            'spreadsheetId': self.spreadsheet_id,
            'valueRenderOption': payload.body['valueRenderOption'],
        }

        if 'dateTimeRenderOption' in payload.body:
            params['dateTimeRenderOption'] = payload.body['dateTimeRenderOption']

        req = self.service.values().batchGet(**params)

        return self(req, transport=transport)

    def batch_values_update(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a batch values update request. note: values.update differs from update."""

        params = {
            'spreadsheetId': self.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.values().batchUpdate(**params)

        return self(req, transport=transport)

    def batch_values_clear(self, payload: googlesheets.resource.Request, transport: 'httplib2.Http' = None) -> dict:
        """submit a batch values clear request."""

        params = {
            'spreadsheetId': self.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.values().batchClear(**params)

        return self(req, transport=transport)
