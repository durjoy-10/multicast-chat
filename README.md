# Multicast Chat Tool

A real-time multicast chat application built with Python, Flask, and WebSockets that allows multiple users to communicate simultaneously.

## Features

- Real-time message broadcasting to all connected users
- User join/leave notifications
- Online users list
- Message history
- Responsive web interface

## How to Run the Project

### Prerequisites
- Python 3.8+
- pip

### Start the Server and Client

1. Open a terminal and start the server:

```bash
cd server
python3 app.py
```

This installs server dependencies (from `server/requirements.txt`) and starts the Socket.IO server on port 5000.

2. In a second terminal, start the client web interface:

```bash
cd client
python3 run_client.py
```

This starts a small Flask app that serves the web UI on http://localhost:5001 and opens it in your browser.

### How it works
- The server (port 5000) runs Flask-SocketIO and handles join/send/receive events.
- The client UI (port 5001) connects to the Socket.IO server and provides the chat interface.

If you want to run both sites from the same machine, make sure ports 5000 and 5001 are available.
