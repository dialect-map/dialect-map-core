#!/bin/sh

# Script safety flags
set -o errexit
set -o nounset

# Define variables
PROJECT_DIR="$(dirname "$0")/.."

# Launches gunicorn
gunicorn \
    --bind "0.0.0.0:8080" \
    --config "${PROJECT_DIR}/src/gunicorn.py" \
    --chdir "${PROJECT_DIR}/src" \
    "main:app"
