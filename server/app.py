from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'multicast_chat_secret'

# Use threading (works on Python 3.13)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Room, users, messages
users = {}
chat_rooms = {
    'multicast-room': {
        'name': 'Multicast Chat Room',
        'users': set(),
        'messages': []
    }
}

@app.route('/')
def index():
    return "Multicast Chat Server is running!"

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    if user_id in users:
        username = users[user_id]['username']
        room = users[user_id]['room']

        # Remove user from room list
        chat_rooms[room]['users'].discard(user_id)

        # Notify others
        emit('user_left', {
            'username': username,
            'message': f'{username} left the chat',
            'timestamp': datetime.datetime.now().isoformat(),
            'user_count': len(chat_rooms[room]['users'])
        }, room=room)

        del users[user_id]

    print(f"Client disconnected: {user_id}")

@socketio.on('join')
def handle_join(data):
    username = data.get('username', f'User_{request.sid[:6]}')
    room = 'multicast-room'

    users[request.sid] = {'username': username, 'room': room}

    join_room(room)
    chat_rooms[room]['users'].add(request.sid)

    emit('user_joined', {
        'username': username,
        'message': f'{username} joined the chat',
        'timestamp': datetime.datetime.now().isoformat(),
        'user_count': len(chat_rooms[room]['users'])
    }, room=room)

    # Send chat history
    for msg in chat_rooms[room]['messages'][-50:]:
        emit('receive_message', msg, room=request.sid)

@socketio.on('send_message')
def handle_send_message(data):
    user_id = request.sid
    if user_id not in users:
        return

    username = users[user_id]['username']
    room = users[user_id]['room']

    # FIX ➜ Python uses strip(), not trim()
    message = data.get('message', '').strip()

    if not message:
        return

    msg_data = {
        'id': len(chat_rooms[room]['messages']) + 1,
        'username': username,
        'message': message,
        'timestamp': datetime.datetime.now().isoformat(),
        'user_id': user_id
    }

    chat_rooms[room]['messages'].append(msg_data)

    emit('receive_message', msg_data, room=room)

@socketio.on('get_users')
def handle_get_users():
    room = 'multicast-room'
    user_list = [users[u]['username'] for u in chat_rooms[room]['users']]
    emit('users_list', {'users': user_list})


if __name__ == '__main__':
    print("Starting Multicast Chat Server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
