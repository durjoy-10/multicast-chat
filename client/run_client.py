#!/usr/bin/env python3
from flask import Flask, render_template
import webbrowser
import threading
import time
#!/usr/bin/env python3
from flask import Flask, render_template
import webbrowser
import threading
import time

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5001')

if __name__ == '__main__':
    print("Starting Multicast Chat Client...")
    print("Opening web interface in browser...")
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the client web server
    app.run(host='127.0.0.1', port=5001, debug=False)