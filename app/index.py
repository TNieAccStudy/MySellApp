from app import app, dao, login, admin, utils
from flask import render_template, request, redirect, session, jsonify
import math
from flask_login import login_user, logout_user, current_user


def run_server():
    app.run(debug=True)


@app.route("/")
def home_page():
    kw = request.args.get('kw')
    page = request.args.get('page', default=1)
    products = dao.get_products(kw,int(page))
    page_size = app.config['PAGE_SIZE']
    page_number = math.ceil(dao.total_products()/page_size)
    return render_template("index.html",
                           pros=products,
                           pgn = page_number,
                           cur_user=current_user)


@app.route("/products/<product_id>")
def details(product_id):
    return render_template('details.html',
                           product=dao.get_product_by_id(product_id),
                           comments=dao.load_comment(product_id))


@app.route("/login", methods=['get','post'])
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')

        u = dao.auth_user(username=username, password=password)
        
        if u:
            login_user(u)
            return redirect("/")
    
    return render_template('login.html',cur_user=current_user)


@app.route("/login-admin", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    
    u = dao.auth_user(username=username,password=password)
    
    if u:
        login_user(u)
    
    return redirect('/admin')


@app.route("/register",methods=['get','post'])
def register_process():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        if password.__eq__(confirm_password):
            data = request.form.copy()
            del data['confirm-password']
            avatar = request.files.get('avatar')
            dao.add_user(avatar=avatar, **data)
        else:
            err_msg= "YOUR PASSWORD NOT FIT"
        return redirect('/login')

    return render_template('register.html', err_msg=err_msg)


@app.route("/logout",methods=['get'])
def logout_process():
    logout_user()
    return redirect("/login")


@app.route("/cart")
def load_cart():
    return render_template('cart.html', 
                           cur_user=current_user,
                           session=session)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/api/products/<product_id>/comments', methods=['post'])
def post_comment(product_id): #lack check comment
    c = dao.add_comment(content=request.json.get('content'), product_id=product_id)
    return jsonify({
        'content': c.content,
        'created_date': c.created_date,
        'user': {
            'avatar': c.user.avatar
        }
        })


@app.route('/api/carts', methods=['post'])
def add_to_cart():
    # """
    # {
    #     "1": {
    #         "id": "1"
    #         "name": "..",
    #         "price": 123,
    #         "quantity": 2
    #     }, 
    #     "2": {
    #         "id": "2"
    #         "name": "..",
    #         "price": 123,
    #         "quantity": 1
    #     }
    # }
    # """
    cart = session.get('cart')
    if not cart:
        cart = {}
    
    p_id = str(request.json.get('id'))
    p_name = request.json.get('name')
    p_price = request.json.get('price')

    if p_id in cart:
        cart[p_id]['quantity']+=1
    else:
        cart[p_id] = {
            "id": p_id,
            "name": p_name,
            "price": p_price,
            "quantity": 1
        }

    session['cart'] = cart
    return jsonify(utils.stats_cart(cart))


@app.route('/api/carts/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = quantity
    
    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/carts/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart
    return jsonify(utils.stats_cart(cart))


@app.context_processor
def common_response():
    return {
        'cart_stats': utils.stats_cart(cart=session.get('cart'))
    }


if __name__ == "__main__":
    run_server()

