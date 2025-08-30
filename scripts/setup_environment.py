#!/usr/bin/env python3
"""
Setup script for AI Interview Assistant
This script helps set up the development environment and check dependencies.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def check_ollama_installation():
    """Check if Ollama is installed and accessible."""
    try:
        result = subprocess.run(['ollama', 'list'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama is installed and accessible")
            return True
        else:
            print("❌ Ollama is installed but not working properly")
            return False
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        print("   Please install Ollama from: https://ollama.ai/")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama is not responding")
        return False


def check_ollama_models():
    """Check if required Ollama models are available."""
    required_models = ['gemma3:4b']
    
    try:
        result = subprocess.run(['ollama', 'list'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return False
        
        available_models = result.stdout.lower()
        missing_models = []
        
        for model in required_models:
            if model.lower() not in available_models:
                missing_models.append(model)
        
        if missing_models:
            print(f"❌ Missing required models: {', '.join(missing_models)}")
            print("   Run the following commands to install:")
            for model in missing_models:
                print(f"   ollama pull {model}")
            return False
        else:
            print("✅ All required Ollama models are available")
            return True
            
    except Exception as e:
        print(f"❌ Error checking Ollama models: {e}")
        return False


def check_dependencies():
    """Check if all Python dependencies are installed."""
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    missing_packages = []
    
    with open(requirements_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                package_name = line.split('>=')[0].split('==')[0].split('[')[0]
                
                # Handle package name mapping
                import_name = package_name
                if package_name == 'faiss-cpu':
                    import_name = 'faiss'
                elif package_name == 'sentence-transformers':
                    import_name = 'sentence_transformers'
                elif package_name == 'python-dotenv':
                    import_name = 'dotenv'
                
                try:
                    importlib.import_module(import_name)
                except ImportError:
                    missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing Python packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All Python dependencies are installed")
        return True


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(__file__).parent.parent / ".env"
    env_example_file = Path(__file__).parent.parent / ".env.example"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example_file.exists():
        import shutil
        shutil.copy(env_example_file, env_file)
        print("✅ Created .env file from template")
        print("   Please review and update the .env file with your settings")
        return True
    else:
        print("❌ .env.example file not found")
        return False


def test_streamlit():
    """Test if Streamlit can import the main application."""
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import src.main
        print("✅ Main application can be imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Error importing main application: {e}")
        return False


def run_setup():
    """Run all setup checks."""
    print("🚀 Setting up AI Interview Assistant...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Dependencies", check_dependencies),
        ("Ollama Installation", check_ollama_installation),
        ("Ollama Models", check_ollama_models),
        ("Environment File", create_env_file),
        ("Application Import", test_streamlit)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        result = check_func()
        results.append((check_name, result))
    
    print("\n" + "="*50)
    print("SETUP SUMMARY")
    print("="*50)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:.<30} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nYou can now run the application:")
        print("   streamlit run src/main.py")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(run_setup())