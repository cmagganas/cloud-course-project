# API Design Checklist - RESTful Endpoint Design

## Implement HTTP

- [ ] Use HTTP methods, i.e. GET, PUT, DELETE, etc.
  - [ ] Use query parameters for filtering, sorting, and pagination in GET requests.
  - [ ] Use request body for POST and PUT requests. Do not use query parameters.
- [ ] Return meaningful status codes indicating the nature of the request success. No need to consider failure cases for this assignment. We will consider those in a later assignment.
- [ ] For GET requests, support pagination, sorting, and filtering using query parameters where appropriate

## Follow formal REST (largely covered by implementing HTTP "right")

- [ ] Uniform Interface
  - [ ] Use standard HTTP methods
  - [ ] Use standard HTTP status codes
  - [ ] Use standard HTTP headers
  - [ ] Implement HATEOAS (rarely done in practice, don't worry about it for this assignment)
- [ ] Stateless
  - [ ] Do not store client state on the server
- [ ] Client-Server decoupling
  - [ ] Ensure that the server is not dependent on details of the client.
        You could write tests from the perspective of a client that is unaware
        of the server's implementation details. This is a good testing practice
        anyway.
- [ ] Cacheable - Use caching headers where appropriate to limit requests made to the API server
- [ ] Layered System - Hide implementation details about the server, and services that the server calls out to, e.g. AWS S3 from the client

## Unofficial REST standards

- [ ] Use resource-oriented design, i.e. nouns for URLs and plural nouns for collections of resources. (e.g. `/users`, `/users/1`)

## Extra

- [ ] Rudimentary data validation and schema documentation (using Pydantic models). A later assignment will focus more in-depth on data validation. For now, just create basic pydantic models.
- [ ] Implement unit tests from the perspective of a client that is unaware of the server's implementation details


