#!/bin/bash

echo "Updating apt repositories..."
sudo apt-get update || { echo "Failed to update apt repositories"; exit 1; }

echo "Installing apt dependencies..."
sudo xargs -a packages.txt apt-get install -y || { echo "Failed to install apt dependencies"; exit 1; }

echo "Activating Python virtual environment..."
source /home/adminuser/venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

echo "Installing Python dependencies..."
pip install -r requirements.txt || { echo "Failed to install Python dependencies"; exit 1; }

echo "Setup completed successfully!"
