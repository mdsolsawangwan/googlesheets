#!/usr/bin/env python

# pylint: disable=fixme

import pathlib

import httplib2
import apiclient

import oauth2client.service_account

from googlesheets import request

class Client(object):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

    def __init__(self, spreadsheet_id: str) -> None:
        self.json_keyfile = None
        self.service = None

        self.cached_spreadsheet = None # cached spreadsheet object

        self.spreadsheet_id = spreadsheet_id

    def initialise(self, json_keyfile: pathlib.Path) -> None:
        """instantiate the service client and complete authorization via oauth2 flow."""

        self.json_keyfile = json_keyfile

        args = [
            str(self.json_keyfile),
            Client.SCOPES,
        ]

        credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(*args)

        args = [
            'sheets',
            'v4'
        ]

        params = {
            'http': credentials.authorize(httplib2.Http()),
            'discoveryServiceUrl': Client.DISCOVERY_URL,
        }

        self.service = apiclient.discovery.build(*args, **params).spreadsheets()

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

    def batch_update(self, payload: request.RequestBody) -> dict:
        """submit a batch update request. primarily used to create new sheets within the current spreadsheet."""

        params = {
            'spreadsheetId': payload.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.batchUpdate(**params)

        try:
            return req.execute()
        except Exception:
            raise

    def batch_values_update(self, payload: request.RequestBody) -> dict:
        """submit a batch values update request. primarily used to write new rows to a sheet."""

        params = {
            'spreadsheetId': payload.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.values().batchUpdate(**params)

        try:
            return req.execute()
        except Exception:
            raise

    def batch_values_clear(self, payload: request.RequestBody) -> dict:
        """submit a batch values clear request. primarily used to delete existing rows from a sheet."""

        params = {
            'spreadsheetId': payload.spreadsheet_id,
            'body': payload.body,
        }

        req = self.service.values().batchClear(**params)

        try:
            return req.execute()
        except Exception:
            raise
