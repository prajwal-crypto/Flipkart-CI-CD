from flask import Flask, render_template, jsonify, request, session
import json

app = Flask(__name__)
app.secret_key = "flipkart-secret-key-2025"

# Sample product data
PRODUCTS = [
    {"id": 1, "name": "Samsung Galaxy S24", "price": 79999, "original_price": 99999, "category": "mobiles", "rating": 4.5, "reviews": 2341, "image": "📱", "brand": "Samsung", "discount": 20},
    {"id": 2, "name": "Apple iPhone 15", "price": 79900, "original_price": 89900, "category": "mobiles", "rating": 4.7, "reviews": 5621, "image": "📱", "brand": "Apple", "discount": 11},
    {"id": 3, "name": "OnePlus 12", "price": 64999, "original_price": 69999, "category": "mobiles", "rating": 4.4, "reviews": 1823, "image": "📱", "brand": "OnePlus", "discount": 7},
    {"id": 4, "name": "Dell Inspiron 15", "price": 54990, "original_price": 72990, "category": "laptops", "rating": 4.3, "reviews": 987, "image": "💻", "brand": "Dell", "discount": 25},
    {"id": 5, "name": "HP Pavilion x360", "price": 62990, "original_price": 79990, "category": "laptops", "rating": 4.2, "reviews": 654, "image": "💻", "brand": "HP", "discount": 21},
    {"id": 6, "name": "MacBook Air M2", "price": 114900, "original_price": 119900, "category": "laptops", "rating": 4.8, "reviews": 3421, "image": "💻", "brand": "Apple", "discount": 4},
    {"id": 7, "name": "Sony WH-1000XM5", "price": 26990, "original_price": 34990, "category": "electronics", "rating": 4.6, "reviews": 4123, "image": "🎧", "brand": "Sony", "discount": 23},
    {"id": 8, "name": "boAt Rockerz 450", "price": 1299, "original_price": 3990, "category": "electronics", "rating": 4.1, "reviews": 12345, "image": "🎧", "brand": "boAt", "discount": 67},
    {"id": 9, "name": "Nike Air Max 270", "price": 9995, "original_price": 12995, "category": "fashion", "rating": 4.4, "reviews": 876, "image": "👟", "brand": "Nike", "discount": 23},
    {"id": 10, "name": "Levi's 511 Slim Jeans", "price": 2099, "original_price": 3999, "category": "fashion", "rating": 4.3, "reviews": 5432, "image": "👖", "brand": "Levi's", "discount": 48},
    {"id": 11, "name": "LG 43\" 4K Smart TV", "price": 32990, "original_price": 54990, "category": "electronics", "rating": 4.4, "reviews": 2109, "image": "📺", "brand": "LG", "discount": 40},
    {"id": 12, "name": "Instant Pot Duo 7-in-1", "price": 8999, "original_price": 12999, "category": "home", "rating": 4.6, "reviews": 3210, "image": "🍲", "brand": "Instant Pot", "discount": 31},
]

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/api/products')
def get_products():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').lower()
    filtered = PRODUCTS
    if category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    if search:
        filtered = [p for p in filtered if search in p['name'].lower() or search in p['brand'].lower()]
    return jsonify(filtered)

@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def cart():
    if 'cart' not in session:
        session['cart'] = []
    if request.method == 'GET':
        return jsonify(session['cart'])
    if request.method == 'POST':
        data = request.json
        cart = session['cart']
        existing = next((item for item in cart if item['id'] == data['id']), None)
        if existing:
            existing['qty'] += 1
        else:
            cart.append({**data, 'qty': 1})
        session['cart'] = cart
        session.modified = True
        return jsonify({'success': True, 'count': len(session['cart'])})
    if request.method == 'DELETE':
        data = request.json
        session['cart'] = [item for item in session['cart'] if item['id'] != data['id']]
        session.modified = True
        return jsonify({'success': True})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'app': 'Flipkart Clone', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
