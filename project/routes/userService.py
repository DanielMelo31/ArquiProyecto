from flask import Blueprint, request, jsonify
from dbConn import get_connection

user_bp = Blueprint('user_bp', __name__)

# Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

# Get user by ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# Create user
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user (user_id, user_name, phone, address) VALUES (%s, %s, %s, %s)",
        (data['user_id'], data['user_name'], data['phone'], data['address'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

# Update user
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user SET user_name=%s, phone=%s, address=%s WHERE user_id=%s",
        (data['user_name'], data['phone'], data['address'], user_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated successfully"})

# Delete user
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE user_id=%s", (user_id,))
    cursor.execute("SET innodb_lock_wait_timeout = 50;")

    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"})
