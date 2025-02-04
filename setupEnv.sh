#!/bin/bash

# Define the virtual environment name
ENV_NAME="qiskit_env"

# Create and activate a virtual environment
echo "Setting up Python virtual environment: $ENV_NAME..."
python3 -m venv $ENV_NAME
source $ENV_NAME/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Qiskit
#echo "Installing Qiskit..."
#pip install -U qiskit

echo "Environment setup complete!"
