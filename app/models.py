from app import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from enum import Enum as EnumType
from datetime import datetime
import hashlib


class UserRole(EnumType):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), 
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name



class Category(db.Model):
    __tablename__ = 'Category'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description =  Column(String(255), nullable= True)
    price = Column(Float, default=0)
    image = Column(String(100), default="https://res.cloudinary.com/duiwbkm7z/image/upload/v1734494876/m6gujsywduy23c5bkv6u.jpg")
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Comment(db.Model):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default= datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)

    def __str__(self):
        return self.content


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # u1=User(name="Admin",username="admin",password='123456',user_role=UserRole.ADMIN)
        # u2=User(name='User1',username='username1',password='123456')
        # db.session.add_all([u1,u2])
        # db.session.commit()

        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # c3 = Category(name='Desktop')

        # db.session.add_all([c1,c2,c3])
        # db.session.commit()


        # data = [{
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2021",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2022",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2023",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2024",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }]

        # for p in data:
            # product = Product(**p)
            # db.session.add(product)
        #     p["name"]+="-2"
        #     product2 = Product(**p)

        #     db.session.add(product2)

        # db.session.commit()


