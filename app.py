from flask import Flask, jsonify
from models import db
from queries import get_users_last_30_days, top_3_products_by_purchase, revenue_by_category, transaction_summaries, users_exceeding_500, remaining_stock

# Initialize the Flask application
app = Flask(__name__)

# Set up the database URI (replace with your actual PostgreSQL credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:Post%40123@localhost:5432/todos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# API Routes
@app.route('/users/purchases/last_30_days', methods=['GET'])
def get_users_last_30_days_api():
    result = get_users_last_30_days()
    return jsonify(result)

@app.route('/products/top_3_by_purchase', methods=['GET'])
def top_3_products_by_purchase_api():
    result = top_3_products_by_purchase()
    return jsonify(result)

@app.route('/products/revenue_by_category', methods=['GET'])
def revenue_by_category_api():
    result = revenue_by_category()
    return jsonify(result)

@app.route('/transactions/summaries', methods=['GET'])
def transaction_summaries_api():
    result = transaction_summaries()
    return jsonify(result)

@app.route('/users/exceeding_500', methods=['GET'])
def users_exceeding_500_api():
    result = users_exceeding_500()
    return jsonify(result)

@app.route('/products/remaining_stock/<int:product_id>', methods=['GET'])
def remaining_stock_api(product_id):
    result = remaining_stock(product_id)
    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
