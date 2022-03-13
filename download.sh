#!/bin/bash

[ -z "$S3_LOCATION" ] && { echo "S3_LOCATION is missing"; exit 1;  }
[ -z "$DOWNLOAD_DIRECTORY" ] && { echo "DOWNLOAD_DIRECTORY is missing"; exit 1;  }

aws s3 cp --recursive "$S3_LOCATION" "$DOWNLOAD_DIRECTORY" || exit 1
gzip -fd $(find "$DOWNLOAD_DIRECTORY" -name "*.gz")
