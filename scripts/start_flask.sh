#!/bin/sh

# Script safety flags
set -o errexit
set -o nounset

# Define default values
flask_env=${FLASK_ENV:-"development"}

# Set up environment variables
export FLASK_ENV=${flask_env}

# Launches Flask
flask run --host "0.0.0.0"
