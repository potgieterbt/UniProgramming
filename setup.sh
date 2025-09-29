#!/bin/bash

# get name from cli
#

for i in "$@"; do
  case i in
    -n=* | --name=*)
      PROJECT_NAME="${i#*=}"
      shift
      ;;
    -p=* | --path=*)
      FULL_PATH="${i#*=}"
      shift
      ;;
    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
  esac
done

# Set the project name (change this if needed)
# PROJECT_NAME="myproject"
VENV_DIR="$HOME/University/Programming/$PROJECT_NAME/myenv"

# Create the project folder if it doesn't exist
mkdir -p "$HOME/University/Programming/$PROJECT_NAME"

# Check if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📌 Creating virtual environment in $VENV_DIR..."
    python -m venv "$VENV_DIR"
    echo "✅ Virtual environment created!"
else
    echo "⚡ Virtual environment already exists. Activating..."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip and install required packages
echo "📦 Installing necessary packages..."
pip install --upgrade pip

echo "🚀 Virtual environment is ready!"
echo "To deactivate, type: deactivate"
