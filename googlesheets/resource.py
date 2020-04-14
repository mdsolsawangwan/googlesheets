#!/usr/bin/env python
"""
googlesheets api v4 request objects.
"""

import abc
import json
import typing
import collections

import googlesheets.notation

query_parameter = collections.namedtuple(
    'query_parameter',
    ('parameter_name', 'parameter_value')
)

class Request(metaclass=abc.ABCMeta):
    """base class for all request payload objects."""

    def __init__(self) -> None:
        self.body = {}

    def __str__(self) -> str:
        return json.dumps(self.body, indent=1, default=str)

class Body(Request):
    """represents a payload for a a non-batched request."""

    def __init__(self, value_range: googlesheets.notation.a1, *query_parameters: query_parameter, validate: bool = True) -> None:
        if validate and not googlesheets.notation.is_valid_syntax(value_range):
            raise SyntaxWarning(f'invalid a1 notation: {value_range}')

        super().__init__()

        self.value_range = value_range
        self.body['range'] = value_range

        for q in query_parameters:
            self.body[q.parameter_name] = q.parameter_value

class BatchBody(Request):
    """represents a payload for a batched request."""

    def __init__(self, key: str, *query_parameters: query_parameter) -> None:
        """a `key` string is assumed to be valid request body key as defined in the sheets api spec."""

        super().__init__()

        self.key = key
        self.body[key] = []

        for q in query_parameters:
            self.body[q.parameter_name] = q.parameter_value

    def append(self, *values: typing.Any) -> None:
        """append one or more values to the request body. child classes define the shape of an expected value."""

        for v in values:
            self.body[self.key].append(v)

class BatchUpdate(BatchBody):
    """note, this differs from `spreadsheet.values().batchUpdate`."""

    def __init__(self) -> None:
        super().__init__('requests')

class ValuesGetFormatted(Body):
    query_parameters = [
        query_parameter('valueRenderOption', 'FORMATTED_VALUE'),
    ]

    def __init__(self, value_range: str) -> None:
        super().__init__(value_range, *ValuesGetFormatted.query_parameters)

class ValuesGetUnformatted(Body):
    query_parameters = [
        query_parameter('valueRenderOption', 'UNFORMATTED_VALUE'),
    ]

    def __init__(self, value_range: str) -> None:
        super().__init__(value_range, *ValuesGetFormatted.query_parameters)

class ValuesGetFormula(Body):
    query_parameters = [
        query_parameter('valueRenderOption', 'FORMULA'),
    ]

    def __init__(self, value_range: str) -> None:
        super().__init__(value_range, *ValuesGetFormatted.query_parameters)

class ValuesUpdateRaw(Body):
    query_parameters = [
        query_parameter('valueInputOption', 'RAW'),
    ]

    def __init__(self, value_range: str, value_range_body: list) -> None:
        super().__init__(value_range, *ValuesUpdateRaw.query_parameters)

        self.body['body'] = {
            'values': [value_range_body],
        }

class ValuesUpdateUserEntered(Body):
    query_parameters = [
        query_parameter('valueInputOption', 'USER_ENTERED'),
    ]

    def __init__(self, value_range: str, value_range_body: list) -> None:
        super().__init__(value_range, *ValuesUpdateUserEntered.query_parameters)

        self.body['body'] = {
            'values': [value_range_body],
        }

class ValuesAppendRaw(Body):
    query_parameters = [
        query_parameter('valueInputOption', 'RAW'),
    ]

    def __init__(self, value_range: str, value_range_body: list, value_input_option: str = None) -> None:
        if value_input_option not in {'OVERWRITE', 'INSERT_ROWS'}:
            value_input_option = 'INSERT_ROWS'

        qp = query_parameter('valueInputOption', value_input_option)

        super().__init__(value_range, qp, *ValuesAppendRaw.query_parameters)

        self.body['body'] = {
            'values': [value_range_body],
        }

class ValuesAppendUserEntered(Body):
    query_parameters = [
        query_parameter('valueInputOption', 'USER_ENTERED'),
    ]

    def __init__(self, value_range: str, value_range_body: list, value_input_option: str = None) -> None:
        if value_input_option not in {'OVERWRITE', 'INSERT_ROWS'}:
            value_input_option = 'INSERT_ROWS'

        qp = query_parameter('valueInputOption', value_input_option)

        super().__init__(value_range, qp, *ValuesAppendUserEntered.query_parameters)

        self.body['body'] = {
            'values': [value_range_body],
        }

class ValuesBatchGetFormatted(BatchBody):
    """
    shape:

        str
    """

    query_parameters = [
        query_parameter('valueRenderOption', 'FORMATTED_VALUE'),
    ]

    def __init__(self) -> None:
        super().__init__('ranges', *ValuesBatchGetFormatted.query_parameters)

class ValuesBatchGetUnformatted(BatchBody):
    """
    shape:

        str
    """

    query_parameters = [
        query_parameter('valueRenderOption', 'UNFORMATTED_VALUE'),
    ]

    def __init__(self, datetime_render_option: str = None) -> None:
        if datetime_render_option not in {'SERIAL_NUMBER', 'FORMATTED_STRING'}:
            datetime_render_option = 'SERIAL_NUMBER'

        qp = query_parameter('dateTimeRenderOption', datetime_render_option)

        super().__init__('ranges', qp, *ValuesBatchGetUnformatted.query_parameters)

class ValuesBatchGetFormula(BatchBody):
    """
    shape:

        str
    """

    query_parameters = [
        query_parameter('valueRenderOption', 'FORMULA'),
    ]

    def __init__(self, datetime_render_option: str = None) -> None:
        if datetime_render_option not in {'SERIAL_NUMBER', 'FORMATTED_STRING'}:
            datetime_render_option = 'SERIAL_NUMBER'

        qp = query_parameter('dateTimeRenderOption', datetime_render_option)

        super().__init__('ranges', qp, *ValuesBatchGetFormula.query_parameters)

class ValuesBatchUpdateRaw(BatchBody):
    """
    shape:

        {
            "range": str,
            "values": [
                list
            ]
        }
    """

    query_parameters = [
        query_parameter('valueInputOption', 'RAW'),
    ]

    def __init__(self) -> None:
        super().__init__('data', *ValuesBatchUpdateRaw.query_parameters)

class ValuesBatchUpdateUserEntered(BatchBody):
    """
    shape:

        {
            "range": str,
            "values": [
                list
            ]
        }
    """

    query_parameters = [
        query_parameter('valueInputOption', 'USER_ENTERED')
    ]

    def __init__(self) -> None:
        super().__init__('data', *ValuesBatchUpdateUserEntered.query_parameters)

class ValuesBatchClear(BatchBody):
    """
    shape:

        str
    """

    def __init__(self) -> None:
        super().__init__('ranges')

################################################################################
# an alternative design that more closely mirrors the sheets api
#
####
    # class Request(metaclass=abc.ABCMeta):
    #     def __init__(self) -> None:
    #         self.body = {}

    #     def __str__(self) -> str:
    #         return json.dumps(
    #             self.body,
    #             indent=1,
    #             default=str,
    #         )

    # class Spreadsheets(Request):
    #     pass

    # class SpreadsheetsSheets(Request):
    #     pass

    # class SpreadsheetsValues(Request):
    #     pass

    # class SpreadsheetsDeveloperMetadata(Request):
    #     pass

    # class Get(Spreadsheets):
    #     pass

    # class BatchUpdate(Spreadsheets):
    #     pass

    # class ValuesGet(SpreadsheetsValues):
    #     pass

    # class ValuesUpdate(SpreadsheetsValues):
    #     pass

    # class ValuesBatchUpdate(SpreadsheetsValues):
    #     pass
###
#
################################################################################