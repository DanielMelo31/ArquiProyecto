from flask import Flask
from routes.userService import user_bp
from routes.productService import product_bp
from routes.orderService import order_bp

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)

# HTTPS config se hace en run.py
