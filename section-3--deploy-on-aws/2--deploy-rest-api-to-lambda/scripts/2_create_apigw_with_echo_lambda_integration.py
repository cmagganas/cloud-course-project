"""
1. create an API Gateway
2. create a Python lambda function that echos back the event
3. create a /echo resource
4. add an ANY method that uses the lambda function as an integration
"""

import json
import os
import time
import zipfile

import boto3
from botocore.exceptions import ClientError

# Configure AWS environment
os.environ["AWS_PROFILE"] = "cloud-course"

# Derive AWS region from environment variable
aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")

# Create clients for API Gateway, Lambda, and IAM
api_client = boto3.client("apigateway", region_name=aws_region)
lambda_client = boto3.client("lambda", region_name=aws_region)
iam_client = boto3.client("iam", region_name=aws_region)
sts_client = boto3.client("sts")

# Get AWS account ID
account_id = sts_client.get_caller_identity()["Account"]

# 0. Create IAM Role for Lambda
role_name = "LambdaExecutionRole"
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}],
}

try:
    role_response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy),
        Description="Role for Lambda execution with basic permissions",
    )

    # Attach policies to the role
    iam_client.attach_role_policy(
        RoleName=role_name, PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    )

    # Wait until the role is created and policies are attached
    time.sleep(10)  # Simple sleep to ensure role creation; consider using waiter for a more robust solution

    role_arn = role_response["Role"]["Arn"]
    print(f"IAM Role ARN: {role_arn}")
    print(
        f"IAM Console URL: https://{aws_region}.console.aws.amazon.com/iam/home?region={aws_region}#/roles/{role_name}"
    )

except ClientError as e:
    if e.response["Error"]["Code"] == "EntityAlreadyExists":
        role_arn = iam_client.get_role(RoleName=role_name)["Role"]["Arn"]
        print(f"Role already exists. Using existing role ARN: {role_arn}")
    else:
        raise

# 1. Create a REST API
api_response = api_client.create_rest_api(
    name="EchoAPI", description="An API that echoes back the event", endpointConfiguration={"types": ["REGIONAL"]}
)
api_id = api_response["id"]
print(
    f"API Gateway Console URL: https://{aws_region}.console.aws.amazon.com/apigateway/home?region={aws_region}#/apis/{api_id}/resources"
)

# Get the root resource id
resources = api_client.get_resources(restApiId=api_id)
root_id = next(item["id"] for item in resources["items"] if item["path"] == "/")

# 2. Create a Python lambda function that echos back the event
lambda_function_name = "EchoFunction"
lambda_handler_code = """
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
"""

# Create a zip file with the lambda function code
with open("/tmp/lambda_function.py", "w") as f:
    f.write(lambda_handler_code)
with zipfile.ZipFile("/tmp/lambda_function.zip", "w") as z:
    z.write("/tmp/lambda_function.py", "lambda_function.py")

# Delete the Lambda function if it exists
try:
    lambda_client.delete_function(FunctionName=lambda_function_name)
    print(f"Deleted existing Lambda function: {lambda_function_name}")
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceNotFoundException":
        print(f"Lambda function {lambda_function_name} does not exist. Proceeding to create a new one.")
    else:
        raise

# Create the Lambda function
lambda_response = lambda_client.create_function(
    FunctionName=lambda_function_name,
    Runtime="python3.12",
    Role=role_arn,
    Handler="lambda_function.lambda_handler",
    Code={"ZipFile": open("/tmp/lambda_function.zip", "rb").read()},
    Publish=True,
)
lambda_arn = lambda_response["FunctionArn"]
print(
    f"Lambda Console URL: https://{aws_region}.console.aws.amazon.com/lambda/home?region={aws_region}#/functions/{lambda_function_name}"
)

# 3. Create a /echo resource
echo_resource_response = api_client.create_resource(restApiId=api_id, parentId=root_id, pathPart="echo")
echo_id = echo_resource_response["id"]
print(
    f"Resource URL: https://{aws_region}.console.aws.amazon.com/apigateway/home?region={aws_region}#/apis/{api_id}/resources/{echo_id}"
)

# 4. Add an ANY method that uses the lambda function as an integration
api_client.put_method(restApiId=api_id, resourceId=echo_id, httpMethod="ANY", authorizationType="NONE")

api_client.put_integration(
    restApiId=api_id,
    resourceId=echo_id,
    httpMethod="ANY",
    type="AWS_PROXY",
    integrationHttpMethod="POST",
    uri=f"arn:aws:apigateway:{aws_region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations",
)

api_client.put_method_response(
    restApiId=api_id,
    resourceId=echo_id,
    httpMethod="ANY",
    statusCode="200",
    responseModels={"application/json": "Empty"},
)

api_client.put_integration_response(restApiId=api_id, resourceId=echo_id, httpMethod="ANY", statusCode="200")

# Add permissions to Lambda to allow API Gateway invocation
statement_id = "apigateway-invoke-permission"
try:
    lambda_client.add_permission(
        FunctionName=lambda_function_name,
        StatementId=statement_id,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=f"arn:aws:execute-api:{aws_region}:{account_id}:{api_id}/*/*",
    )
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceConflictException":
        print(f"Permission {statement_id} already exists. Skipping permission addition.")
    else:
        raise

# Create a /prod stage
deployment_response = api_client.create_deployment(
    restApiId=api_id,
    stageName="prod",
    stageDescription="Production stage",
    description="Deployment for the production stage",
)
print(
    f"Stage URL: https://{aws_region}.console.aws.amazon.com/apigateway/home?region={aws_region}#/apis/{api_id}/stages/prod"
)

# Construct the base URL for the deployed API
stage_base_url = f"https://{api_id}.execute-api.{aws_region}.amazonaws.com/prod"
print(f"Stage base URL: {stage_base_url}")
print(f"ANY /echo URL: {stage_base_url}/echo")
