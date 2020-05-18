# Data Cleaning For Skip Tracing

Purpose of these scripts is to ingest data from either listsource or title company (see exmples), and format them such
that complete (clean) data is split from that in need of more digging.

Assuming you create a `data/` dir and put each list within its own dir as well.

## Uploading to Drive
There's also a convenience script here called `upload_to_drive.py` which requires setup of Google Drive API. It allows you to push automatically to a pre-
defined drive. Read [here](https://developers.google.com/drive/api/v3/quickstart/python) for more details. You need to download a `client_id.json` from your
google drive/ cloud console.