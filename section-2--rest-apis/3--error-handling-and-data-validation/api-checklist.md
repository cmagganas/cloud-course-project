# API Design Checklist - Error Handling

## Implement HTTP

- [ ] Return error HTTP status codes. [FastAPI Guide](https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code)

## Error handling

**Principle:** NEVER let your API crash. Always handle exceptions and return a meaningful client-facing response to the client that

- helps them understand what went wrong and how to fix it
- does not reveal internal implementation details of the API

---

- [ ] Globally catch errors and return a meaningful response to the user. [FastAPI Guide](https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers)
  - [ ] Catch `pydantic.ValidationError` as `422 Unprocessable Entity`
  - [ ] Catch `Exception` as `500 Internal Server Error` (as of this writing, FastAPI does not provide a way to catch broad exceptions the same way as other types, see reference code)
- [ ] In error messages, do not reveal implementation details to the user about what went wrong. 
  - **Bad:** `"the file was not found in the S3 bucket at path <...>".` (mentions S3)
  - **Good:** `"the file requested was not found at path <...>."`
- [ ] **(not in this section)** Include a request ID in error messages to give to "the support team" (you). Include it in logs.
- [ ] Unit test that the correct status codes and responses are returned in error cases

## Data validation

**Principle:** assume all API inputs are malicious until proven otherwise.

- [ ] Validate API inputs
  - [ ] Query parameters (for appropriate HTTP methods)
  - [ ] Request body (for appropriate HTTP methods)
  - [ ] Request headers
  - [ ] Path parameters
- [ ] Unit test validation logic

Use Pydantic models wherever possible.

1. [ ] Prefer JSON schema validation wherever possible, e.g.
   ```python
    class GetPeopleRequest(BaseModel):
        min_age: int = Field(..., gt=0)
    ```
2. [ ] Use Pydantic validators for more complex validation. [model_validator guide](https://docs.pydantic.dev/latest/concepts/validators/#model-validators)
   ```python
    class GetPeopleRequest(BaseModel):
        min_age: int = Field(..., gt=0)
        max_age: int = Field(..., lt=100) # no one makes it to 100
        
        @model_validator(mode="before")
        def validate_age_range(cls, values: dict):
            if values["min_age"] > values["max_age"]:
                raise ValueError("min_age must be less than or equal to max_age")
    ```
