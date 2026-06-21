#!/bin/bash

# PURPOSE: used by jenkins to run the code past the linter
set -e -o xtrace

# 1. Normalize image name

# 2. Cleanup function to ensure Jenkins workspace stays clean regardless of success/fail
# shellcheck disable=SC2317
cleanup() {
    echo "Performing cleanup..."
    docker rm -f "${DOCKER_TEST_CONTAINER}" 2>/dev/null || true
    docker image rm -f "${docker_test_image_lower_case}" 2>/dev/null || true
}
# Trap will run the cleanup function on script exit or interrupt
trap cleanup EXIT


export LOCALHOST_TEST_DIR="formatting_results"
export DOCKER_TEST_CONTAINER="git_notification_bot_test"
export docker_test_image_lower_case="git_notification_bot_test"
# 3. Prepare local directories
rm -rf "${LOCALHOST_TEST_DIR}"
mkdir -p "${LOCALHOST_TEST_DIR}"

# 4. Build the test image
docker build --no-cache -t "${docker_test_image_lower_case}" -f Dockerfile.lint  .

echo "Checking for environment file..."
ENV_FILE="git_notification_bot.env"
declare -a ENV_ARGS=() # Initialize an empty array

# Only add the flag if the file exists on the host
if [ -f "$ENV_FILE" ]; then
    echo "Found $ENV_FILE, applying to container."
    ENV_ARGS=("--env-file" "$ENV_FILE") # Add two distinct elements to the array
else
    echo "No env file found at $ENV_FILE, skipping flag."
fi

# 5. Run synchronously (No more while loop!)
# Using --name allows us to reference it for 'cp' afterwards even if it's stopped.
echo "Running validation container..."
docker run --name "${DOCKER_TEST_CONTAINER}" "${ENV_ARGS[@]}" "${docker_test_image_lower_case}"

docker cp "${DOCKER_TEST_CONTAINER}:/src/app/test.xml" "${LOCALHOST_TEST_DIR}/test.xml"

# 6. Capture the exit code immediately
test_exit_code=$(docker inspect "${DOCKER_TEST_CONTAINER}" --format='{{.State.ExitCode}}')

# 8. Handle Failure vs Success
if [ "${test_exit_code}" -ne "0" ]; then
    echo "Validation failed with exit code ${test_exit_code}. Dumping logs:"
    docker logs "${DOCKER_TEST_CONTAINER}"
    exit 1
fi

echo "Validation passed!"
exit 0
