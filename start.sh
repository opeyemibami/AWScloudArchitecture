#!/bin/bash
source env/bin/activate
cd "$(dirname "$0")"
uvicorn main:app --host=0.0.0.0 --workers=1
echo "bash script running"
