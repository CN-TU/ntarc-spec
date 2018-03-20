#!/bin/bash

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

# Verify using the JSON Schema (does not validate features)
hash jsonschema 2>/dev/null || { echo >&2 "Please intall jsonschema: \`pip install jsonschema\`"; exit 1; }
if [ -z "$1" ]
then
    echo "Usage: ./verify.sh FILENAME_TO_TEST.json"
    exit 1
fi
export PYTHONPATH="$SCRIPTPATH"

jsonschema -i $1 $SCRIPTPATH/schema_v2.json && echo "No errors according to JSON Schema!" && \
        python3 $PYTHONPATH/v2_processing/scripts/verify.py $1  # Verify features
