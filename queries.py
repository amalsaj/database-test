from models import db, User, Product, Transaction, TransactionDetail
from sqlalchemy import func
from datetime import datetime, timedelta

# Function to get users with purchases in the last 30 days
def get_users_last_30_days():
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    users = db.session.query(User).join(Transaction).filter(Transaction.date >= thirty_days_ago).all()
    result = [{"user_id": user.user_id, "name": user.name, "email": user.email} for user in users]
    return result

# Function to get the top 3 products by purchase frequency
def top_3_products_by_purchase():
    top_products = db.session.query(Product, func.sum(TransactionDetail.quantity).label('total_quantity')) \
                             .join(TransactionDetail) \
                             .group_by(Product.product_id) \
                             .order_by(func.sum(TransactionDetail.quantity).desc()) \
                             .limit(3).all()
    result = [{"product_id": product.product_id, "name": product.name, "total_quantity": quantity} for product, quantity in top_products]
    return result

# Function to calculate revenue per product category
def revenue_by_category():
    revenue = db.session.query(Product.category, func.sum(TransactionDetail.quantity * Product.price).label('revenue')) \
                        .join(TransactionDetail) \
                        .group_by(Product.category).all()
    result = [{"category": category, "revenue": revenue} for category, revenue in revenue]
    return result

# Function to generate transaction summaries with item counts
def transaction_summaries():
    summaries = db.session.query(Transaction.transaction_id, func.count(TransactionDetail.product_id).label('item_count'), 
                                 func.sum(TransactionDetail.quantity * Product.price).label('total_amount')) \
                          .join(TransactionDetail).join(Product) \
                          .group_by(Transaction.transaction_id).all()
    result = [{"transaction_id": trans_id, "item_count": item_count, "total_amount": total_amount} 
              for trans_id, item_count, total_amount in summaries]
    return result

# Function to find users exceeding $500 in total purchases
def users_exceeding_500():
    users = db.session.query(User, func.sum(TransactionDetail.quantity * Product.price).label('total_spent')) \
                      .join(Transaction).join(TransactionDetail).join(Product) \
                      .group_by(User.user_id) \
                      .having(func.sum(TransactionDetail.quantity * Product.price) > 500).all()
    result = [{"user_id": user.user_id, "name": user.name, "total_spent": total_spent} 
              for user, total_spent in users]
    return result

# Function to calculate the remaining stock for a product
def remaining_stock(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404
    
    sold_quantity = db.session.query(func.sum(TransactionDetail.quantity)) \
                              .filter(TransactionDetail.product_id == product_id).scalar() or 0
    remaining_stock = product.stock - sold_quantity
    return {"product_id": product_id, "remaining_stock": remaining_stock}
