#!/bin/bash
echo "bash script running"
cd "$(dirname "$0")"
uvicorn main:app --host=0.0.0.0 --workers=4