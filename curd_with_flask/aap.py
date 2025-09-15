from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
import uuid

app = Flask(__name__)
CORS(app)
# SQL Server connection configuration
def get_db_connection():
    conn = pyodbc.connect(
        'driver=ODBC Driver 17 for SQL Server;'
        'server=SIPL147\\SQLEXPRESS;'  # double backslash for escape
        'database=db_test;'
        'Trusted_Connection=yes;'
    )
    return conn

# Create table if not exists
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
        CREATE TABLE Users (
            id UNIQUEIDENTIFIER PRIMARY KEY,
            name NVARCHAR(100),
            email NVARCHAR(100),
            age INT
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Initialize database
init_db()

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        
        if not all([name, email, age]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        user_id = str(uuid.uuid4())
        
        cursor.execute(
            "INSERT INTO Users (id, name, email, age) VALUES (?, ?, ?, ?)",
            (user_id, name, email, age)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'id': user_id,
            'name': name,
            'email': email,
            'age': age
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Users")
        users = [
            {
                'id': str(row[0]),
                'name': row[1],
                'email': row[2],
                'age': row[3]
            }
            for row in cursor.fetchall()
        ]
        
        cursor.close()
        conn.close()
        
        return jsonify(users), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Read a specific user
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Users WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({
                'id': str(row[0]),
                'name': row[1],
                'email': row[2],
                'age': row[3]
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a user
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Users WHERE id = ?", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'User not found'}), 404
            
        update_query = "UPDATE Users SET "
        params = []
        if name:
            update_query += "name = ?, "
            params.append(name)
        if email:
            update_query += "email = ?, "
            params.append(email)
        if age:
            update_query += "age = ?, "
            params.append(age)
            
        update_query = update_query.rstrip(', ') + " WHERE id = ?"
        params.append(id)
        
        cursor.execute(update_query, tuple(params))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'User updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a user
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Users WHERE id = ?", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'User not found'}), 404
            
        cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)