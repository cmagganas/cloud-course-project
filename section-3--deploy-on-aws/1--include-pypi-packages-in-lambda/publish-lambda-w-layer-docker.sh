set -ex

# arn:aws:lambda:us-west-2:905418322705:layer:cloud-course-project-python-deps:1

# aws lambda publish-layer-version --layer-name cloud-course-project-python-deps --compatible-runtimes python3.12 --zip-file fileb://lambda-layer.zip --compatible-architectures arm64 --profile cloud-course --region us-west-2

# clean up artifacts
rm -rf lambda-env || true
rm -f lambda-layer.zip || true

# install dependencies
docker logout || true  # log out to use the public ecr
docker pull public.ecr.aws/lambda/python:3.12-arm64

docker run --rm \
    --volume $(pwd):/out \
    --entrypoint /bin/bash \
    public.ecr.aws/lambda/python:3.12-arm64 \
    -c ' \
    pip install \
        -r /out/requirements.txt \
        --target /out/lambda-env/python \
    '

# bundle dependencies and handler in a zip file
cd lambda-env
zip -r ../lambda-layer.zip ./

cd ../src
zip -r ../lambda.zip ./

cd ..

# cp lambda_function.py lambda-env/
# # publish the zip file
export AWS_PROFILE=default
export AWS_REGION=us-east-2
aws lambda update-function-code \
    --function-name demo-function \
    --zip-file fileb://./lambda.zip \
    --output json | cat

LAYER_VERSION_ARN=$(aws lambda publish-layer-version \
    --layer-name cloud-course-project-python-deps \
    --compatible-runtimes python3.12 \
    --zip-file fileb://lambda-layer.zip \
    --compatible-architectures arm64 \
    --query 'LayerVersionArn' \
    --output text | cat)

aws lambda update-function-configuration \
    --function-name demo-function \
    --layers $LAYER_VERSION_ARN \
    --output json | cat