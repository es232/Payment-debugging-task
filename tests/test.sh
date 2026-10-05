#!/bin/bash
set -e

# Navigate to the root of the task directory
cd "$(dirname "$0")/.."

echo "Building Docker environment..."
docker build -t api-payout-task -f environment/Dockerfile .

echo "Running test suite..."
# We mount app.py so the AI agent's edits are reflected inside the container
docker run --rm \
    -v "$(pwd)/environment/app.py:/app/app.py" \
    -v "$(pwd)/tests:/app/tests" \
    api-payout-task pytest tests/test_outputs.py -v
