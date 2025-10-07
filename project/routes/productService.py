from flask import Blueprint, request, jsonify
from dbConn import get_connection

product_bp = Blueprint('product_bp', __name__)

# Get all products
@product_bp.route('/products', methods=['GET'])
def get_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

# Get product by ID
@product_bp.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

# Create product
@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    required_fields = ['product_id', 'product_name', 'description', 'price', 'inventory']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO product (product_id, product_name, description, price, inventory) VALUES (%s, %s, %s, %s, %s)",
        (data['product_id'], data['product_name'], data['description'], data['price'], data['inventory'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Product created successfully"}), 201

# Update product
@product_bp.route('/products/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE product SET product_name=%s, description=%s, price=%s, inventory=%s WHERE product_id=%s",
        (data['product_name'], data['description'], data['price'], data['inventory'], product_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Product updated successfully"})

# Delete product
@product_bp.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE product_id=%s", (product_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product deleted successfully"})

# Check stock of a product
@product_bp.route('/products/<string:product_id>/stock', methods=['GET'])
def check_stock(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_name, inventory FROM product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "product": product['product_name'],
        "inventory": product['inventory']
    })

# Update inventory (increment or decrement)
@product_bp.route('/products/<string:product_id>/inventory', methods=['PATCH'])
def update_inventory(product_id):
    data = request.get_json()
    change = data.get('change', 0)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE product SET inventory = inventory + %s WHERE product_id = %s", (change, product_id))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Inventory updated by {change} units"})
