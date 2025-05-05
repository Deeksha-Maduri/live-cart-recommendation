from flask import Flask, render_template
from app.utils.fetch_products import get_products
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from search import search_products
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    products = get_products()
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)

df = pd.read_csv('data/products.csv')

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return 'Item added to cart', 200

@app.route('/cart')
def cart():
    cart_items = df[df['id'].isin(session.get('cart', []))]
    return render_template('cart.html', items=cart_items.to_dict(orient='records'))

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    results = search_products(query)
    return jsonify(results[['title', 'price']].to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

