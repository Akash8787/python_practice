from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# Secret key to encode/decode JWT
SECRET_KEY = 'your-secret-key'

# Simulated user (you can add DB logic instead)
USER = {
    'username': 'admin',
    'password': '1234'
}

# Generate token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == USER['username'] and data['password'] == USER['password']:
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify(token=token)
    else:
        return jsonify(message="Invalid credentials"), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization') or request.headers.get('authorization')

    if token is None:
        return jsonify(message="Missing token"), 403

    try:
        token = token.replace("Bearer ", "").strip()
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify(message="Access granted", user=decoded['user'])
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(message="Invalid token"), 401

if __name__ == '__main__':
    app.run(debug=True)
