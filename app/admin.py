from flask_admin import BaseView, Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from app import app, db, admin, dao
from app.models import Category, User, Product, Comment, UserRole
from flask_login import current_user, logout_user
from flask import redirect


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', cur_user=current_user, stats=dao.products_stats())


admin = Admin(app=app, name="eConmerce", 
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class CategoryView(AdminView):
    can_view_details = True
    column_list = ['name', 'products']


class ProductView(AdminView):
    column_list = ['name','category_id', 
                   'description', 'price',
                   'image']
    column_sortable_list = ['name', 'price']
    column_filters = ['name', 'price']
    column_editable_list = ['name', 'price', 'description']
    can_set_page_size = True
    create_modal = True


class UserView(AdminView):
    column_list = ['name', 'username','user_role']
    can_view_details = True
    column_editable_list = ['name', 'user_role']


class CommentView(AdminView):
    column_list = ['user_id', 'product_id', 'content', 'created_date']
    column_editable_list = ['content']


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
    

class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    

# class StatsView(AuthenticatedView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/stats.html',)


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product,db.session))
admin.add_view(UserView(User,db.session))
admin.add_view(CommentView(model=Comment, session=db.session))
admin.add_view(LogoutView(name="LOGOUT"))