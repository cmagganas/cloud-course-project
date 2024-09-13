#!/bin/bash

set -e

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# start the FastAPI app, enabling hot reload on save (assuming files_api packages is installed)
function run {
    AWS_PROFILE=cloud-course uvicorn src.files_api.main:APP --reload
}

# start the FastAPI app, pointed at a mocked aws endpoint
function run-mock {
    set +e

    # Start moto.server in the background on localhost:5000
    python -m moto.server -p 5000 &
    MOTO_PID=$!

    # point the AWS CLI and boto3 to the mocked AWS server using mocked credentials
    export AWS_ENDPOINT_URL="http://localhost:5000"
    export AWS_SECRET_ACCESS_KEY="mock"
    export AWS_ACCESS_KEY_ID="mock"

    # create a bucket called "some-bucket" using the mocked aws server
    aws s3 mb s3://some-bucket

    # Trap EXIT signal to kill the moto.server process when uvicorn stops
    trap 'kill $MOTO_PID' EXIT

    # Set AWS endpoint URL and start FastAPI app with uvicorn in the foreground
    uvicorn src.files_api.main:APP --reload

    # Wait for the moto.server process to finish (this is optional if you want to keep it running)
    wait $MOTO_PID
}

# start the FastAPI app, enabling hot reload on save (assuming files_api packages is not installed)
function run-py {
    AWS_PROFILE=cloud-course  PYTHONPATH="${THIS_DIR}/src" uvicorn files_api.main:APP --reload
}


# (example) ./run.sh test tests/test_states_info.py::test__slow_add
function run-tests {
    PYTEST_EXIT_STATUS=0
    rm -rf "$THIS_DIR/test-reports" || true
    python -m pytest ${@:-"$THIS_DIR/tests/"} \
        --cov "${COVERAGE_DIR:-$THIS_DIR/src}" \
        --cov-report html \
        --cov-report term \
        --cov-report xml \
        --junit-xml "$THIS_DIR/test-reports/report.xml" \
        --cov-fail-under 60 || ((PYTEST_EXIT_STATUS+=$?))
    mv coverage.xml "$THIS_DIR/test-reports/" || true
    mv htmlcov "$THIS_DIR/test-reports/" || true
    mv .coverage "$THIS_DIR/test-reports/" || true
    return $PYTEST_EXIT_STATUS
}


TIMEFORMAT="Task completed in %3lR"
time ${@:-help}
