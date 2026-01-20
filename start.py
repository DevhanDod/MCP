"""
Improved startup script for MCP Application
"""
import sys
import os
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required = {
        'flask': 'Flask',
        'pandas': 'pandas', 
        'numpy': 'numpy',
        'tensorflow': 'tensorflow',
        'sklearn': 'scikit-learn',
        'kagglehub': 'kagglehub'
    }
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n🔧 Fix: Run one of these commands:")
        print("   pip install -r requirements.txt")
        print("   OR")
        print("   ./run.sh")
        return False
    return True

def check_model_exists():
    """Check if trained model exists"""
    return os.path.exists("saved_model") and os.path.exists("preprocessor.pkl")

def main():
    print("="*70)
    print("🚀 MCP - Menstrual Cycle Prediction Application")
    print("="*70)
    print()
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher required")
        print(f"   Current version: {sys.version.split()[0]}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies installed")
    
    # Check if model is trained
    print("🔍 Checking for trained model...")
    if not check_model_exists():
        print("❌ Model not found!")
        print()
        print("="*70)
        print("📚 FIRST TIME SETUP REQUIRED")
        print("="*70)
        print()
        print("The model needs to be trained once (takes 2-5 minutes).")
        print()
        response = input("Would you like to train the model now? (yes/no): ")
        
        if response.lower() in ['yes', 'y']:
            print()
            print("="*70)
            print("🧠 Training model...")
            print("="*70)
            print()
            
            # Run training script
            result = subprocess.run([sys.executable, "train_model.py"])
            
            if result.returncode != 0:
                print()
                print("❌ Model training failed!")
                sys.exit(1)
            
            print()
            print("="*70)
            print("✅ Model trained successfully!")
            print("="*70)
        else:
            print()
            print("To train the model manually, run:")
            print("   python train_model.py")
            print()
            print("Then restart this script:")
            print("   python start.py")
            sys.exit(0)
    else:
        print("✅ Trained model found")
    
    # Start Flask app
    print()
    print("="*70)
    print("🌟 Starting web server...")
    print("="*70)
    print()
    
    try:
        from app import app, load_model
        
        # Load model
        if not load_model():
            print()
            print("❌ Failed to load model!")
            sys.exit(1)
        
        print()
        print("="*70)
        print("✨ Application ready!")
        print("="*70)
        print()
        print("🌐 Open your browser and visit:")
        print("   👉 http://localhost:5000")
        print()
        print("📱 Or use your device on the same network:")
        print("   👉 http://<your-ip>:5000")
        print()
        print("Press Ctrl+C to stop the server")
        print("="*70)
        print()
        
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print()
        print("="*70)
        print("❌ CRITICAL ERROR")
        print("="*70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("="*70)
        sys.exit(1)

if __name__ == "__main__":
    main()
