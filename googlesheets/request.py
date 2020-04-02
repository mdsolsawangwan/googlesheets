#!/usr/bin/env python
"""
googlesheets api v4 request objects.
"""

import json
import typing

field = typing.Tuple[str, str]
fields = typing.List[field]

class RequestBody(object):
    """base class for a googlesheets api request body."""

    def __init__(self, request_body_key: str, required_fields: fields = None) -> None:
        """`required_fields` is a list of key-value pair tuples."""

        self.request_body_key = request_body_key

        self.body = {
            request_body_key: []
        }

        if required_fields:
            for k, v in required_fields:
                self.body[k] = v

    def __str__(self) -> str:
        return json.dumps(self.body, indent=1, default=str)

    def append(self, *requests: typing.Any) -> None:
        """append one or more values to the request body. child classes define the shape of an expected value."""

        for r in requests:
            self.body[self.request_body_key].append(r)

# class RequestRead(RequestBody):
#     def __init__(self, datetime_render_option: str = None) -> None:
#         if datetime_render_option not in {'SERIAL_NUMBER', 'FORMATTED_STRING'}:
#             datetime_render_option = 'SERIAL_NUMBER'

#         super().__init__(
#             'ranges',
#             required_fields=[
#                 ('valueRenderOption', 'UNFORMATTED_VALUE'),
#                 ('dateTimeRenderOption', datetime_render_option),
#             ]
#         )

# class RequestWrite(RequestBody):
#     def __init__(self, request_body_key: str) -> None:


class BatchUpdate(RequestBody):
    """note, this differs from `spreadsheet.values().batchUpdate`."""

    def __init__(self) -> None:
        super().__init__('requests')

class BatchGetValuesFormatted(RequestBody):
    """
    fetch multiple row ranges, returned text retains cell formatting.

    calls to `.append()` take an object with the following shape:

        str
    """

    def __init__(self) -> None:
        super().__init__(
            'ranges',
            required_fields=[
                ('valueRenderOption', 'FORMATTED_VALUE'),
            ]
        )

class BatchGetValuesUnformatted(RequestBody):
    """
    fetch multiple row ranges, returned text ignores cell formatting.

    calls to `.append()` take an object with the following shape:

        str
    """

    def __init__(self, datetime_render_option: str = None) -> None:
        if datetime_render_option not in {'SERIAL_NUMBER', 'FORMATTED_STRING'}:
            datetime_render_option = 'SERIAL_NUMBER'

        super().__init__(
            'ranges',
            required_fields=[
                ('valueRenderOption', 'UNFORMATTED_VALUE'),
                ('dateTimeRenderOption', datetime_render_option),
            ]
        )

class BatchGetValuesFormula(RequestBody):
    """
    fetch multiple row ranges, returned text is raw.

    calls to `.append()` take an object with the following shape:

        str
    """

    def __init__(self, datetime_render_option: str = None) -> None:
        if datetime_render_option not in {'SERIAL_NUMBER', 'FORMATTED_STRING'}:
            datetime_render_option = 'SERIAL_NUMBER'

        super().__init__(
            'ranges',
            required_fields=[
                ('valueRenderOption', 'FORMULA'),
                ('dateTimeRenderOption', datetime_render_option),
            ]
        )

class BatchUpdateValuesRaw(RequestBody):
    """
    write multiple rows, raw text.

    calls to `.append()` take an object with the following shape:

        {
            "range": str,
            "values": [
                list
            ]
        }
    """

    def __init__(self) -> None:
        super().__init__(
            'data',
            required_fields=[
                ('valueInputOption', 'RAW')
            ]
        )

class BatchUpdateValuesUserEntered(RequestBody):
    """
    write multiple rows, formatted text.

    calls to `.append()` take an object with the following shape:

        {
            "range": str,
            "values": [
                list
            ]
        }
    """

    def __init__(self) -> None:
        super().__init__(
            'data',
            required_fields=[
                ('valueInputOption', 'USER_ENTERED')
            ]
        )

class BatchUpdateValuesClear(RequestBody):
    """
    clear multiple ranges.

    calls to `.append()` take an object with the following shape:

        str
    """

    def __init__(self) -> None:
        super().__init__('ranges')
