# googlesheets

* * *

## about

a small `python` wrapper client for the `googlesheets` v4 api.

## usage

  - _create a `googlesheets.api.Client`_
  ```python
  client = googlesheets.api.Client('SPREADSHEET_ID')
  ```
  - _load the client credentials_
  ```python
  client.initialise('./PATH/TO/KEY_FILE.json')
  ```
  - _clear all rows in a sheet except the first_
  ```python
  batch_clear = googlesheets.request.BatchUpdateValuesClear(client.spreadsheet_id)
  batch_clear.append('SHEET_NAME!A2:Z')

  print(client.batch_values_clear(batch_clear))
  ```
  - _write rows starting from the second_
  ```python
  batch_update = googlesheets.request.BatchUpdateValuesRaw(gsc.spreadsheet_id)
  batch_update.append({
        'range': 'SHEET_NAME!A2',
        'values': [
            [...],
            [...],
            ...
        ],
  })

  print(client.batch_values_update(batch_update))
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
