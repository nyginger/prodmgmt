# -*- coding: utf-8 -*-


from flask_restless import APIManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
#from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
import os
from eins_app import app,db
from models import LimitModelView,Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen,LotView,WorkView





#db_adapter=SQLAlchemyAdapter(db,Persons)
#user_manager=UserManager(db_adapter,app)


admin=Admin(app, template_mode='bootstrap3')
admin.add_view(LotView(Lot, db.session))
admin.add_view(WorkView(Works, db.session))
admin.add_view(LimitModelView(Product, db.session))
admin.add_view(LimitModelView(Company, db.session))
admin.add_view(LimitModelView(Persons, db.session))
admin.add_view(ModelView(Stage, db.session))


apimanager=APIManager(app,flask_sqlalchemy_db=db)
apimanager.create_api(Persons, methods=['GET','POST','PUT', 'DELETE'])
apimanager.create_api(Works, methods=['GET','POST', 'PUT', 'DELETE'])
apimanager.create_api(Lot, methods=['GET','POST','PUT', 'DELETE'],results_per_page=1000)
apimanager.create_api(Stage, methods=['GET','POST', 'DELETE'],results_per_page=1000)
apimanager.create_api(Stage_procs,methods=['GET','POST','PUT','DELETE'], results_per_page=1000)
apimanager.create_api(Company,methods=['GET','POST','PUT','DELETE'], results_per_page=1000)
apimanager.create_api(Product,methods=['GET','POST','PUT','DELETE'], results_per_page=1000)

