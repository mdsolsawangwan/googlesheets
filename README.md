# googlesheets

* * *

## about

a small `python` wrapper client for the `googlesheets` v4 api.

## usage

  - _create a `googlesheets.api.Client`_
  ```python
  client = googlesheets.api.Client('SPREADSHEET_ID')
  client.init('./PATH/TO/KEY_FILE.json') # load credentials and create a service object
  ```
  - _create a new sheet tab_
  ```python
  req = googlesheets.resource.BatchUpdate()

  req.append({
      'addSheet': {
          'properties': {
              'title': sheet_name,
              'gridProperties': {
                  'rowCount': row_count
              }
          }
      }
  })

  res = client.batch_update(req) # json response
  ```
  - _clear all rows in a sheet except the first_
  ```python
  req = googlesheets.resource.BatchUpdateValuesClear()

  req.append('SHEET_NAME!A2:Z')

  res = client.batch_values_clear(req) # json response
  ```
  - _write rows starting including column headers_
  ```python
  req = googlesheets.resource.BatchUpdateValuesRaw()

  req.append({
        'range': 'SHEET_NAME!A1',
        'values': [
            [...], # headers
            [...], # and all the rows ..
            ...
        ],
  })

  res = client.batch_values_update(req) # json response
  ```

## setup

### credentials

currently, only service accounts are supported. in order for the client to authenticate with the `googlesheets` v4 api, a service
account configuration file is required (_a.k.a `json_keyfile`_).

a service account configuration file has the following shape:

```json
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```
