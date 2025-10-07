from flask import Blueprint, request, jsonify
from dbConn import get_connection

order_bp = Blueprint('order_bp', __name__)

# Get all orders
@order_bp.route('/orders', methods=['GET'])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM order_")
    orders = cursor.fetchall()
    conn.close()
    return jsonify(orders)

# Get order by ID
@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM order_ WHERE orderID = %s", (order_id,))
    order = cursor.fetchone()
    conn.close()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

# Create new order
@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = ['orderID', 'user_id', 'date', 'total']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO order_ (orderID, user_id, date, total) VALUES (%s, %s, %s, %s)",
        (data['orderID'], data['user_id'], data['date'], data['total'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Order created successfully"}), 201

# Delete order
@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM order_ WHERE orderID = %s", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order deleted successfully"})
