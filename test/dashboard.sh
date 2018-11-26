#!/usr/bin/env bash

set -o errexit

echo "Executing dashboard.sh script ..."
source .tox/test/bin/activate
cd .tox/test/tmp/
python3 -m coral_dashboard -vvv
