# Create and write to setup.sh
cat << 'EOF' > setup.sh
#!/bin/bash

# Activate the Python virtual environment
echo "Activating virtual environment..."
source /home/adminuser/venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt || { echo "Failed to install Python dependencies"; exit 1; }

echo "Setup completed successfully!"
EOF

# Make the script executable
chmod +x setup.sh

# Confirm the script has been created and is executable
echo "setup.sh has been created and made executable."
