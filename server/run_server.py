#!/usr/bin/env python3
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    #!/usr/bin/env python3
    import subprocess
    import sys
    import os

    def install_requirements():
        """Install required packages"""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Requirements installed successfully!")
        except subprocess.CalledProcessError:
            print("Error installing requirements. Please install manually:")
            print("pip install -r requirements.txt")

    if __name__ == "__main__":
        # Install requirements
        install_requirements()
    
        # Start the server
        print("Starting Multicast Chat Server...")
        from app import socketio, app
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)