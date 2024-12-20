from app.models import Product, Category, User, UserRole, Comment
from app import app, db
import hashlib
from cloudinary import uploader
from sqlalchemy import func
from flask_login import current_user

def get_products(kw, page):
    query = Product.query

    if kw:
        query=query.filter(Product.name.contains(kw))

    page_size = app.config['PAGE_SIZE']
    product_start = page_size*(page-1)
    query = query.slice(start=product_start, stop=product_start+page_size)

    return query


def total_products():
    return Product.query.count()


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    auth_password = password_process(password)
    
    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(auth_password))
    return u.first()


def add_user(name,username,password,avatar):

    def check_user(username):
        return User.query.filter(User.username.__eq__(username)).first()
        
    if not check_user(username):
        password = password_process(password)
        
        u = User(name=name,username=username,password=password,user_role=UserRole.USER)

        if avatar:
            res = uploader.upload(avatar)
            u.avatar = res.get('secure_url')

        db.session.add(u)
        db.session.commit()
        return True
    return False


def password_process(password):
    return hashlib.md5(password.strip().encode("utf-8")).hexdigest()


def products_stats():
    return db.session.query(Category.id,Category.name, func.count(Product.id))\
        .join(Product,Product.category_id.__eq__(Category.id),isouter=True)\
            .group_by(Category.id).all()

    
def get_product_by_id(id):
    return Product.query.get(id)


def load_comment(product_id):
    return Comment.query.filter(Comment.product_id==product_id).order_by(-Comment.id).all()


def add_comment(content, product_id):
    c = Comment(content=content, user_id=current_user.id, product_id=product_id)
    db.session.add(c)
    db.session.commit()
    return c