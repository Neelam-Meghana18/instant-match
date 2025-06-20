# from flask_socketio import SocketIO, emit, join_room 
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import sqlite3

# from yaml import emit

# app = Flask(__name__)
# CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")
# DB_PATH = '../db/users.db'

# waiting_users = []  # List of users waiting to be matched
# matched_users = {}  # Dict of name → match info


# @app.route('/match', methods=['POST'])
# def match():
#     try:
#         data = request.get_json()
#         name = data.get('name', '').strip()
#         age = data.get('age')
#         issue = data.get('issue', '').strip().lower()
#         language = data.get('language', '').strip().lower()

#         if not name or not issue or not language:
#             return jsonify({"error": "Missing required fields"}), 400

#         # Save user to DB
#         conn = sqlite3.connect(DB_PATH)
#         c = conn.cursor()
#         c.execute('INSERT INTO users (name, age, issue, language) VALUES (?, ?, ?, ?)',
#                   (name, age, issue, language))
#         conn.commit()
#         conn.close()

#         # Check if there's a matching user
#         for i, user in enumerate(waiting_users):
#             if (
#                 user['issue'] == issue and
#                 user['language'] == language and
#                 user['name'] != name
#             ):
#                 matched_user = waiting_users.pop(i)

#                 # Save match for both users
#                 matched_users[name] = {
#                     "name": matched_user['name'],
#                     "age": matched_user['age'],
#                     "issue": matched_user['issue'],
#                     "language": matched_user['language'],
#                     "photo": "👤"
#                 }

#                 matched_users[matched_user['name']] = {
#                     "name": name,
#                     "age": age,
#                     "issue": issue,
#                     "language": language,
#                     "photo": "👤"
#                 }

#                 print(f"✅ Match found: {name} ↔ {matched_user['name']}")
#                 return jsonify(matched_users[name])

#         # If no match found, add to waiting list
#         waiting_users.append({
#             "name": name,
#             "age": age,
#             "issue": issue,
#             "language": language
#         })

#         print(f"⏳ Added {name} to waiting_users")
#         return jsonify({"error": "No match found yet, waiting..."})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/check-match', methods=['GET'])
# def check_match():
#     name = request.args.get('name', '').strip()
#     if not name:
#         return jsonify({"error": "Name required"}), 400

#     if name in matched_users:
#         return jsonify(matched_users[name])
#     else:
#         return jsonify({"error": "Still waiting..."}), 404


# # @app.route('/send', methods=['POST'])
# # def send_message():
# #     data = request.get_json()
# #     sender = data.get("sender")
# #     receiver = data.get("receiver")
# #     message = data.get("message")

# #     if not sender or not receiver or not message:
# #         return jsonify({"error": "All fields required"}), 400

# #     conn = sqlite3.connect(DB_PATH)
# #     c = conn.cursor()
# #     c.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
# #               (sender, receiver, message))
# #     conn.commit()
# #     conn.close()

# #     return jsonify({"success": True})


# # @app.route('/messages', methods=['GET'])
# # def get_messages():
# #     sender = request.args.get('sender')
# #     receiver = request.args.get('receiver')

# #     if not sender or not receiver:
# #         return jsonify({"error": "Sender and receiver required"}), 400

# #     conn = sqlite3.connect(DB_PATH)
# #     c = conn.cursor()
# #     c.execute('''
# #         SELECT sender, receiver, message, timestamp 
# #         FROM messages 
# #         WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?) 
# #         ORDER BY timestamp ASC
# #     ''', (sender, receiver, receiver, sender))
# #     messages = c.fetchall()
# #     conn.close()

# #     return jsonify([
# #         {"sender": m[0], "receiver": m[1], "message": m[2], "timestamp": m[3]} for m in messages
# #     ])
# # === Realtime Chat Events ===
# @socketio.on('join_room')
# def handle_join(data):
#     username = data['username']
#     partner = data['partner']
#     room = get_room_name(username, partner)
#     join_room(room)
#     emit('chat_message', {"sender": "System", "message": f"{username} joined the chat."}, room=room)

# @socketio.on('send_message')
# def handle_send(data):
#     sender = data['sender']
#     receiver = data['receiver']
#     message = data['message']
#     room = get_room_name(sender, receiver)

#     # Save message to DB
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)", (sender, receiver, message))
#     conn.commit()
#     conn.close()

#     emit('chat_message', {"sender": sender, "message": message}, room=room)

# def get_room_name(user1, user2):
#     return '_'.join(sorted([user1, user2]))

# if __name__ == '__main__':
#     socketio.run(app, debug=True, port=5000)

# from flask import Flask, render_template, request
# from flask_socketio import SocketIO, emit, join_room
# from flask_cors import CORS
# import uuid

# app = Flask(__name__)
# CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # In-memory user store (temporary)
# waiting_users = []
# active_rooms = {}

# @app.route('/')
# def index():
#     return "Instant Match Server is running"

# # Helper to create room name
# def get_room_name(user1, user2):
#     if not user1 or not user2:
#         print("Error: Missing user1 or user2 in get_room_name")
#         return None
#     return '_'.join(sorted([user1, user2]))

# # Handle user match request
# @app.route('/match', methods=['POST'])
# def match():
#     data = request.json

#     # Safely extract and clean input
#     username = data.get('username', '').strip()
#     issue = data.get('issue', '').strip().lower()
#     language = data.get('language', '').strip().lower()

#     # ✅ Validation
#     if not username or not issue or not language:
#         print("❌ Invalid match request: missing fields.")
#         return {
#             "matched": False,
#             "error": "All fields (username, issue, language) are required."
#         }, 400

#     print(f"📥 Received match request: {username} | {issue} | {language}")

#     # 🔍 Try to find a matching user
#     for i, user in enumerate(waiting_users):
#         if user['issue'] == issue and user['language'] == language:
#             partner = waiting_users.pop(i)
#             room = get_room_name(username, partner['username'])

#             if room:
#                 active_rooms[room] = [username, partner['username']]
#                 print(f"✅ Match found: {username} ↔ {partner['username']} in room {room}")
#                 return {
#                     "matched": True,
#                     "room": room,
#                     "partner": partner['username']
#                 }

#     # 🕒 No match — add to waiting list
#     waiting_users.append({
#         "username": username,
#         "issue": issue,
#         "language": language
#     })

#     print(f"⏳ No match found for {username}, added to waiting_users.")
#     return {"matched": False}

# @app.route('/check-match', methods=['GET'])
# def check_match():
#     username = request.args.get('name')
#     print(f"Checking match for: {username}")

#     for room, users in active_rooms.items():
#         if username in users:
#             partner = users[1] if users[0] == username else users[0]
#             return {
#                 "matched": True,
#                 "room": room,
#                 "name": partner
#             }

#     return {
#         "matched": False
#     }, 404


# # Handle client joining chat room
# @socketio.on('join')
# def handle_join(data):
#     username = data.get('username')
#     partner = data.get('partner')

#     print(f"[JOIN] {username} wants to join with {partner}")

#     room = get_room_name(username, partner)
#     if room:
#         join_room(room)
#         emit('chat_message', {
#             "sender": "System",
#             "message": f"{username} joined the chat."
#         }, room=room)
#     else:
#         print("Error: Room could not be created because username or partner is missing")

# # Handle chat message
# @socketio.on('send_message')
# def handle_message(data):
#     username = data.get('username')
#     partner = data.get('partner')
#     message = data.get('message')

#     room = get_room_name(username, partner)
#     if room:
#         print(f"[MESSAGE] {username} to {partner}: {message}")
#         emit('chat_message', {
#             "sender": username,
#             "message": message
#         }, room=room)
#     else:
#         print("Error: Cannot send message, room is None")

# # Main entry
# if __name__ == '__main__':
#     from os import getenv
#     app.run(host="0.0.0.0", port=int(getenv("PORT", 5000)))
from flask import Flask, request, jsonify
from flask_cors import CORS
import pusher

pusher_client = pusher.Pusher(
  app_id='2010934',
  key='8685cf11979ffbaa7ea6',
  secret='34b43b122f64f4dad71c',
  cluster='ap2',
  ssl=True
)

app = Flask(__name__)
CORS(app)

# In-memory match tracking
waiting_users = []
active_rooms = {}

@app.route('/')
def index():
    return "💡 Instant Match Server is running (no sockets)"

def get_room_name(user1, user2):
    return '_'.join(sorted([user1, user2]))

@app.route('/match', methods=['POST'])
def match():
    data = request.json

    username = data.get('username', '').strip()
    issue = data.get('issue', '').strip().lower()
    language = data.get('language', '').strip().lower()

    if not username or not issue or not language:
        return jsonify({
            "matched": False,
            "error": "All fields (username, issue, language) are required"
        }), 400

    print(f"📥 Match request: {username}, {issue}, {language}")

    for i, user in enumerate(waiting_users):
        if user['issue'] == issue and user['language'] == language and user['username'] != username:
            partner = waiting_users.pop(i)
            room = get_room_name(username, partner['username'])

            active_rooms[username] = {
                "matched": True,
                "room": room,
                "name": partner['username']
            }
            active_rooms[partner['username']] = {
                "matched": True,
                "room": room,
                "name": username
            }

            print(f"✅ Match made: {username} ↔ {partner['username']} in room {room}")
            return jsonify(active_rooms[username])

    # No match found
    waiting_users.append({
        "username": username,
        "issue": issue,
        "language": language
    })

    print(f"⏳ {username} added to waiting_users")
    return jsonify({"matched": False})

@app.route('/check-match', methods=['GET'])
def check_match():
    username = request.args.get('name', '').strip()
    print(f"🔍 Checking for match: {username}")

    if username in active_rooms:
        return jsonify(active_rooms[username])

    return jsonify({"matched": False}), 404
@app.route('/leave', methods=['POST'])
def leave_chat():
    data = request.json
    username = data.get('username')
    
    # Remove user from any room they're part of
    to_delete = []
    for room, users in active_rooms.items():
        if username in users:
            to_delete.append(room)

    for room in to_delete:
        del active_rooms[room]
    
    print(f"❌ {username} has left the chat. Room(s) cleaned.")
    return {"success": True}

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')

    room = get_room_name(sender, receiver)

    pusher_client.trigger(room, 'new_message', {
        'sender': sender,
        'message': message
    })

    return {"success": True}

if __name__ == '__main__':
    from os import getenv
    app.run(host='0.0.0.0', port=int(getenv("PORT", 5000)))
