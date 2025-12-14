# FraudGuard Labs Setup Script

import os
import subprocess
import sys

def install_dependencies():
    """Install required dependencies from requirements.txt"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True

def create_models_directory():
    """Create the models directory for storing trained models"""
    models_dir = "fraudguard_app/models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created directory: {models_dir}")
    else:
        print(f"Directory already exists: {models_dir}")

def main():
    """Main setup function"""
    print("Setting up FraudGuard Labs...")
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Please check your requirements.txt file.")
        return
    
    # Create necessary directories
    create_models_directory()
    
    print("\nSetup complete!")
    print("\nTo run the application:")
    print("  streamlit run app.py")
    
    print("\nTo run tests:")
    print("  python -m pytest fraudguard_app/tests/")

if __name__ == "__main__":
    main()