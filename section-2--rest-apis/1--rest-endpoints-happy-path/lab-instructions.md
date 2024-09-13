# Lab: Implement the "happy path" for Files API Endpoints

In this exercise, you will implement the REST API endpoints for the Files API.

Do not worry about

- documentation (the OpenAPI schema)
- error handling, error response status codes, or data validation, just do the "happy path" AKA assume nothing goes wrong
- using `camelCase` in request/response payloads. `snake_case` is fine for now.
- logging
- versioning

We will come back and implement these in later assignments.

## Assignment

There are 3 main parts to this assignment:

1. Implement the endpoints as shown below by their example requests and responses.
2. For each endpoint, implement the full checklist laid out in [`./api-checklist.md`](./api-checklist.md).
3. Test the happy path for each endpoint

Subsequent assignments will build on this one, adding more polish in their own checklist items.

## Assignment format

Fill in these files

```
hw/
├── src
│   └── files_api
│       └── main.py          # fill in
└── tests
    ├── fixtures
    │   └── mocked_aws.py    # provided, you may edit
    └── unit_tests
        └── test__main.py    # fill in
```

## Endpoints (implement these)

- `PUT /files/{filePath}`: Upload or overwrite a file. (see note below, why we use PUT for both create and update, and do not have a `POST` method)
- `GET /files`: List files metadata with pagination support.
- `GET /files/{filePath}`: Get a file by its path.
- `HEAD /files/{filePath}`: Get metadata of a file by its path (rather than the whole file).
- `DELETE /files/{filePath}`: Delete a file by its path.


> 📌 **Design Note 1:** We are using PUT for both create and update options instead of POST because this API is atypical. In most REST APIs, the POST request accepts data, creates an object, and assigns it an ID. 
> 
> This is good because it's best not to allow users to have control over ID generation, e.g., to help ensure resource IDs are unique among other reasons. The fact that this is a file server makes our API a special case because it makes more sense for an API like this to have the URN be a file path rather than creating a separate URN, e.g., a UUID for each file. 
> 
> File paths already guarantee uniqueness, the ability to look up the resource, etc. So in this case, we use a PUT for both create and update operations. The PUT verb assumes that the URN is known by the user. In our case, it is.

> 📌 **Design Note 2:**
> Technically, the fact that our URI/URNs use exact file paths as they are stored in S3 violates REST somewhat.
> As does the fact that users will likely store files with file extensions, e.g. `path/to/file.csv` which would
> match with a MIME type of `text/csv` in the `Content-Type` header, and therefore implies that the user
> can never request that the file be delivered in another format via `Accept:`.

## Files API Endpoints Specifications

### 1. Upload or Overwrite File

#### Endpoint

```
PUT /files/{filePath}
```

#### Request

##### Path Parameters
- `filePath` (required, string): The path of the file to be uploaded or overwritten.

##### Query Parameters
- None

##### Request Body
- Accepts a file in the request body as binary data.

##### Notable Request Headers
- `Content-Type: application/octet-stream` - The MIME type of the file being uploaded, e.g. `text/plain`, `image/jpeg`, etc.

##### Example Request
```bash
PUT /files/myfolder/file1.txt HTTP/1.1
Host: api.example.com
Content-Type: text/plain

(file content here)
```

#### Response

##### Status Codes
- `201 Created`: Returned on successful creation of a new file (where no file existed before).
- `200 OK`: Returned on successful overwrite of an existing file.

##### Notable Response Headers
- None

##### Response Payload (for 201 Created)
- JSON object containing:
  - `filePath` (string): The path of the uploaded file.
  - `message` (string): A message indicating that a new file was uploaded.

##### Example Response (201 Created)
```bash
HTTP/1.1 201 Created
Content-Type: application/json

{
  "filePath": "myfolder/file1.txt",
  "message": "New file uploaded: /path/to/file"
}
```

### 2. List Files

#### Endpoint
```
GET /files
```

#### Request

##### Path Parameters
- None

##### Query Parameters
- `pageSize` (optional, integer, default: 10): The number of files to return per page.
- `directory` (optional, string): The directory to list files from.
- `pageToken` (optional, string): The token for the next page of results.

##### Request Body
- None

##### Notable Request Headers
- None

##### Example Request
```bash
GET /files?pageSize=5&directory=myfolder&pageToken=abc123 HTTP/1.1
Host: api.example.com
```

#### Response

##### Status Codes
- `200 OK`: Returned on successful retrieval of file list.

##### Notable Response Headers
- None

##### Response Payload
- JSON object containing:
  - `files` (array): List of file metadata objects, each containing:
    - `filePath` (string): The path of the file.
    - `lastModified` (string): The last modified date of the file.
    - `sizeBytes` (integer): The size of the file in bytes.
  - `nextPageToken` (string): The token for the next page of results.

##### Example Response
```bash
HTTP/1.1 200 OK
Content-Type: application/json

{
  "files": [
    {
      "filePath": "myfolder/file1.txt",
      "lastModified": "2023-01-01T00:00:00Z",
      "sizeBytes": 12345
    },
    {
      "filePath": "myfolder/file2.txt",
      "lastModified": "2023-01-02T00:00:00Z",
      "sizeBytes": 67890
    }
  ],
  "nextPageToken": "next_page_token_value",
}
```

### 3. Get File

#### Endpoint
```
GET /files/{filePath}
```

#### Request

##### Path Parameters
- `filePath` (required, string): The path of the file to retrieve.

##### Query Parameters
- None

##### Request Body
- None

##### Notable Request Headers
- None

##### Example Request
```bash
GET /files/myfolder/file1.txt HTTP/1.1
Host: api.example.com
```

#### Response

##### Status Codes
- `200 OK`: Returned on successful retrieval of the file.
- `404 Not Found`: Returned if the file is not found.

##### Notable Response Headers
- `Content-Type`: The MIME type of the file.
- `Content-Length`: The size of the file in bytes.

##### Response Payload (for 200 OK)
- Returns the file content with the appropriate MIME type.

##### Example Response (200 OK)
```bash
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 12345

(file content here)
```

### 4. Get File Metadata

#### Endpoint
```
HEAD /files/{filePath}
```

#### Request

##### Path Parameters
- `filePath` (required, string): The path of the file to retrieve metadata for.

##### Query Parameters
- None

##### Request Body
- None

##### Notable Request Headers
- None

##### Example Request
```bash
HEAD /files/myfolder/file1.txt HTTP/1.1
Host: api.example.com
```

#### Response

##### Status Codes
- `200 OK`: Returned on successful retrieval of the file metadata.
- `404 Not Found`: Returned if the file is not found.

##### Notable Response Headers
- `Content-Type`: The MIME type of the file.
- `Content-Length`: The size of the file in bytes.
- `Last-Modified`: The last modified date of the file.

##### Response Payload
- HEAD requests must not return a response payload.

##### Example Response (200 OK)
```bash
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 12345
Last-Modified: 2023-01-01T00:00:00Z
```

### 5. Delete File

#### Endpoint
```
DELETE /files/{filePath}
```

#### Request

##### Path Parameters
- `filePath` (required, string): The path of the file to delete.

##### Query Parameters
- None

##### Request Body
- None

##### Notable Request Headers
- None

##### Example Request
```bash
DELETE /files/myfolder/file1.txt HTTP/1.1
Host: api.example.com
```

#### Response

##### Status Codes
- `204 No Content`: Returned on successful deletion of the file.
- `404 Not Found`: Returned if the file is not found.

##### Notable Response Headers
- None

##### Response Payload
- None

##### Example Response (204 No Content)
```bash
HTTP/1.1 204 No Content
```
