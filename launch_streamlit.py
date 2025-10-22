#!/usr/bin/env python3
"""
Streamlit App Launcher for Gamma Exposure Dashboard
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import plotly
        import yfinance
        print("✅ All required packages are available")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Installing requirements...")
        
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_streamlit.txt"
        ])
        return True

def launch_app():
    """Launch the Streamlit application"""
    print("🚀 Launching Gamma Exposure Dashboard...")
    print("📱 The app will open in your default browser")
    print("🔧 Use Ctrl+C to stop the application")
    print("-" * 50)
    
    # Launch streamlit
    subprocess.run([
        "streamlit", "run", "streamlit_app.py",
        "--server.address", "localhost",
        "--server.port", "8501",
        "--browser.gatherUsageStats", "false"
    ])

if __name__ == "__main__":
    try:
        # Change to script directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Check requirements
        if check_requirements():
            launch_app()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)