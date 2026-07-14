from flask import Flask, render_template, session, redirect, url_for, request
from products import products

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Main route: displays the product list homepage
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Route to add a product to the session-based shopping cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('view_cart'))

# Route to view all items currently in the shopping cart and calculate total
@app.route('/cart')
def view_cart():
    cart_items = []
    total = 0
    for pid in session.get('cart', []):
        product = next((p for p in products if p['id'] == pid), None)
        if product:
            cart_items.append(product)
            total += product['price']
    return render_template('cart.html', cart_items=cart_items, total=total)

# Route to handle order checkout and payment processing
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)
        return render_template('payment_success.html')
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)