"""
Creates the mock integration shown in the videos.

1. creates a REST API gateway
2. adds a /greeting resource
3. configures a mock integration with this response template with a GET method

{
  "message": "hello!",
  "httpMethod": "$context.httpMethod",
  "requestPath": "$context.path"
}

4. creates a /prod stage
"""

import json
import os

import boto3

os.environ["AWS_PROFILE"] = "cloud-course"
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

# Create a client for API Gateway
client = boto3.client("apigateway")

# 1. Create a REST API
api_response = client.create_rest_api(
    name="GreetingAPI", description="An API to greet the user", endpointConfiguration={"types": ["REGIONAL"]}
)
api_id = api_response["id"]
print(
    f"API Gateway Console URL: https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/{api_id}/resources\n"
)

# Get the root resource id
print("Fetching root resource ID...")
resources = client.get_resources(restApiId=api_id)
root_id = next(item["id"] for item in resources["items"] if item["path"] == "/")
print(f"Root resource ID: {root_id}\n")

# 2. Add a /greeting resource
print("Creating /greeting resource...")
greeting_resource_response = client.create_resource(restApiId=api_id, parentId=root_id, pathPart="greeting")
greeting_id = greeting_resource_response["id"]
print(
    f"Resource URL: https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/{api_id}/resources/{greeting_id}\n"
)

# 3. Configure a mock integration with the provided response template for a GET method
response_template = {"message": "hello!", "httpMethod": "$context.httpMethod", "requestPath": "$context.path"}

client.put_method(restApiId=api_id, resourceId=greeting_id, httpMethod="GET", authorizationType="NONE")

client.put_integration(
    restApiId=api_id,
    resourceId=greeting_id,
    httpMethod="GET",
    type="MOCK",
    requestTemplates={"application/json": '{"statusCode": 200}'},
)

client.put_method_response(
    restApiId=api_id,
    resourceId=greeting_id,
    httpMethod="GET",
    statusCode="200",
    responseModels={"application/json": "Empty"},
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=greeting_id,
    httpMethod="GET",
    statusCode="200",
    responseTemplates={"application/json": json.dumps(response_template)},
)

# 4. Create a /prod stage
deployment_response = client.create_deployment(
    restApiId=api_id,
    stageName="prod",
    stageDescription="Production stage",
    description="Deployment for the production stage",
)
print(
    f"Stage URL: https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/{api_id}/stages/prod\n"
)

# Construct the base URL for the deployed API
stage_base_url = f"https://{api_id}.execute-api.us-west-2.amazonaws.com/prod"
print(f"Stage base URL: {stage_base_url}")
print(f"GET /greeting URL: {stage_base_url}/greeting\n")
