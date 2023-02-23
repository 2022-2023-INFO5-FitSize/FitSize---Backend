#!/bin/bash

# Set the URL of the Google Drive archive
url="https://drive.google.com/uc?id=1-OFnoDgnYrkxiB6icgmaOpFQS1TAunfs&export=download"

# Set the local paths for the models and weights folders
models_dir="./keypoints/code/models/models"
weights_dir="./keypoints/code/weights"

# Check if the models and weights directories already contain content
if [ "$(ls -A $models_dir)" ] || [ "$(ls -A $weights_dir)" ]; then
  echo "Models and/or weights files already exist. Skipping download."
  exit 0
fi

# Download the file using gdown
echo "Downloading the archive..."
gdown "$url" -O tmp.zip

# Extract the contents of the archive
echo "Extracting the archive..."
unzip -q tmp.zip -d tmp

# Copy the files to the target directories
echo "Copying files to target directories..."
cp -r tmp/* $models_dir
cp -r tmp/* $weights_dir

# Clean up temporary files
echo "Cleaning up..."
rm -rf tmp.zip tmp

echo "Done."
