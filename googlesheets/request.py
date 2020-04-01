#!/usr/bin/env python
"""
utility classes for constructing api request objects.
"""

import json
import typing

field = typing.Tuple[str, str]
fields = typing.List[field]

class RequestBody(object):
    """base class for a googlesheets api request body."""

    def __init__(self, spreadsheet_id: str, request_body_key: str, required_fields: fields = None):
        """`required_fields` is a list of key-value pair tuples."""

        self.spreadsheet_id = spreadsheet_id
        self.request_body_key = request_body_key

        self.body = {
            request_body_key: []
        }

        if required_fields:
            for k, v in required_fields:
                self.body[k] = v

    def __str__(self):
        return json.dumps({
            'params': {
                'spreadsheet_id': self.spreadsheet_id,
                **self.body,
            }
        }, indent=1, default=str)

    def append(self, *requests: typing.Any):
        """append one or more values to the request body. child classes define the shape of an expected value."""

        for r in requests:
            self.body[self.request_body_key].append(r)

class BatchUpdate(RequestBody):
    """note, this differs from `spreadsheet.values().batchUpdate`."""

    def __init__(self, spreadsheet_id: str) -> None:
        super().__init__(spreadsheet_id, 'requests')

class BatchUpdateValuesRaw(RequestBody):
    """
    for writing rows as raw text.

    calls to `.append()` take an object with the following shape:

        {
            "range": str,
            "values": [
                list
            ]
        }
    """

    def __init__(self, spreadsheet_id: str) -> None:
        super().__init__(
            spreadsheet_id,
            'data',
            required_fields=[
                ('valueInputOption', 'RAW')
            ]
        )

class BatchUpdateValuesUserEntered(RequestBody):
    """
    for writing rows as formatted text.

    calls to `.append()` take an object with the following shape:

        {
            "range": str,
            "values": [
                list
            ]
        }
    """

    def __init__(self, spreadsheet_id: str) -> None:
        super().__init__(
            spreadsheet_id,
            'data',
            required_fields=[
                ('valueInputOption', 'USER_ENTERED')
            ]
        )

class BatchUpdateValuesClear(RequestBody):
    """
    for clearing a range of cells.

    calls to `.append()` take an object with the following shape:

        str
    """

    def __init__(self, spreadsheet_id: str) -> None:
        super().__init__(spreadsheet_id, 'ranges')
