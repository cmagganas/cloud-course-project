# clean up artifacts
rm -rf lambda-env || true
rm -f lambda.zip || true

# install dependencies
pip install --target ./lambda-env requests fastapi

# bundle dependencies and handler in a zip file
cp lambda_function.py lambda-env/
cd lambda-env
zip -r ../lambda.zip ./

# publish the zip file
export AWS_PROFILE=default
export AWS_REGION=us-east-2
aws lambda update-function-code \
    --function-name demo-function \
    --zip-file fileb://../lambda.zip