#!/bin/bash

[ -z "$1" ] && { echo "Usage: $0 s3bucket/s3path"; exit 1; }

export S3_LOCATION=s3://$1
export DOWNLOAD_DIRECTORY=cloudtrail-log
export REPORTS_DIR=reports

[ -d "$REPORTS_DIR" ] && rm "$REPORTS_DIR"/*
mkdir -p "$REPORTS_DIR"

./download.sh || exit 1
./analyze.py "$DOWNLOAD_DIRECTORY" "$REPORTS_DIR" || exit 1
