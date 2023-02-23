#!/bin/bash

# Set the URL of the Google Drive archive
url="https://drive.google.com/uc?id=1-OFnoDgnYrkxiB6icgmaOpFQS1TAunfs&export=download"

# Set the local paths for the models and weights folders
models_dir="./keypoints/code/models/models"
weights_dir="./keypoints/code/weights"

# Check if the target directories already contain content
if [ -n "$(ls -A $models_dir 2>/dev/null)" ] && [ -n "$(ls -A $weights_dir 2>/dev/null)" ]; then
  echo "The target directories already contain content. Exiting."
  exit 0
fi

# Create target directories if they don't exist
if [ ! -d $models_dir ]; then
  echo "Creating $models_dir directory..."
  mkdir -p $models_dir
fi

if [ ! -d $weights_dir ]; then
  echo "Creating $weights_dir directory..."
  mkdir -p $weights_dir
fi

# Download the file using gdown
echo "Downloading the archive..."
gdown "$url" -O tmp.zip

# Extract the contents of the archive
echo "Extracting the archive..."
unzip -q tmp.zip -d tmp

# Copy the files to the target directories
echo "Copying files to target directories..."
cp -r tmp/modelsFitSize.nosync/* $models_dir
cp -r tmp/modelsFitSize.nosync/* $weights_dir

# Clean up temporary files
echo "Cleaning up..."
rm -rf tmp.zip tmp

echo "Done."
