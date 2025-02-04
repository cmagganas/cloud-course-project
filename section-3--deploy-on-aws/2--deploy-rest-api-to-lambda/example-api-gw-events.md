# Example API Gateway Events

API Gateway converts incoming HTTP requests into JSON objects and passes them to the Lambda function to be handled.

Here is a list of example `cURL` requests and their corresponding JSON objects that would be created by API Gateway (specifically the HTTP API).

These objects can be used in the AWS Lambda console as test events to validate the behavior of the Lambda function after wrapping the FastAPI app with `mangum`.

### Upload File - `PUT /v1/files/{file_path}`

```curl
curl -X PUT "https://id.execute-api.us-east-1.amazonaws.com/v1/files/generated/speech.mp3" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/file"
```

See [`./mangum-notebook/put-audio-file-request.json`](./mangum-notebook/put-audio-file-request.json) for an example request.

The example is not included in this file because it is long.

### List Files - `GET /v1/files`

```curl
curl -X GET "https://id.execute-api.us-east-1.amazonaws.com/v1/files?page_size=10&directory=generated" \
     -H "Content-Type: application/json"
```

```json
{
  "version": "2.0",
  "routeKey": "GET /v1/files",
  "rawPath": "/v1/files",
  "rawQueryString": "page_size=10&directory=generated",
  "headers": {
    "Content-Type": "application/json"
  },
  "requestContext": {
    "accountId": "123456789012",
    "apiId": "api-id",
    "http": {
      "method": "GET",
      "path": "/v1/files",
      "protocol": "HTTP/1.1",
      "sourceIp": "192.168.1.1",
      "userAgent": "CustomUserAgentString"
    },
    "requestId": "example-id",
    "routeKey": "GET /v1/files",
    "stage": "prod"
  },
  "queryStringParameters": {
    "page_size": "10",
    "directory": "generated"
  }
}
```

### Get File Metadata - `HEAD /v1/files/{file_path}`

```curl
curl -X HEAD "https://id.execute-api.us-east-1.amazonaws.com/v1/files/generated/speech.mp3" \
     -H "Content-Type: application/json"
```

```json
{
  "version": "2.0",
  "routeKey": "HEAD /v1/files/{file_path}",
  "rawPath": "/v1/files/generated/speech.mp3",
  "rawQueryString": "",
  "headers": {
    "Content-Type": "application/json"
  },
  "requestContext": {
    "accountId": "123456789012",
    "apiId": "api-id",
    "http": {
      "method": "HEAD",
      "path": "/v1/files/generated/speech.mp3",
      "protocol": "HTTP/1.1",
      "sourceIp": "192.168.1.1",
      "userAgent": "CustomUserAgentString"
    },
    "requestId": "example-id",
    "routeKey": "HEAD /v1/files/{file_path}",
    "stage": "prod"
  },
  "pathParameters": {
    "file_path": "generated/speech.mp3"
  }
}
```

### Retrieve File - `GET /v1/files/{file_path}`

```curl
curl -X GET "https://id.execute-api.us-east-1.amazonaws.com/v1/files/generated/speech.mp3" \
     -H "Content-Type: application/json"
```

```json
{
  "version": "2.0",
  "routeKey": "GET /v1/files/{file_path}",
  "rawPath": "/v1/files/generated/speech.mp3",
  "rawQueryString": "",
  "headers": {
    "Content-Type": "application/json"
  },
  "requestContext": {
    "accountId": "123456789012",
    "apiId": "api-id",
    "http": {
      "method": "GET",
      "path": "/v1/files/generated/speech.mp3",
      "protocol": "HTTP/1.1",
      "sourceIp": "192.168.1.1",
      "userAgent": "CustomUserAgentString"
    },
    "requestId": "example-id",
    "routeKey": "GET /v1/files/{file_path}",
    "stage": "prod"
  },
  "pathParameters": {
    "file_path": "generated/speech.mp3"
  }
}
```

### Delete File - `DELETE /v1/files/{file_path}`

```curl
curl -X DELETE "https://id.execute-api.us-east-1.amazonaws.com/v1/files/generated/speech.mp3" \
     -H "Content-Type: application/json"
```

```json
{
  "version": "2.0",
  "routeKey": "DELETE /v1/files/{file_path}",
  "rawPath": "/v1/files/generated/speech.mp3",
  "rawQueryString": "",
  "headers": {
    "Content-Type": "application/json"
  },
  "requestContext": {
    "accountId": "123456789012",
    "apiId": "api-id",
    "http": {
      "method": "DELETE",
      "path": "/v1/files/generated/speech.mp3",
      "protocol": "HTTP/1.1",
      "sourceIp": "192.168.1.1",
      "userAgent": "CustomUserAgentString"
    },
    "requestId": "example-id",
    "routeKey": "DELETE /v1/files/{file_path}",
    "stage": "prod"
  },
  "pathParameters": {
    "file_path": "generated/speech.mp3"
  }
}
```