# -*- coding: utf-8 -*-



from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from prod_app import db




class LimitModelView(ModelView):
    can_delete = False  # disable model deletion
    page_size = 10  # the number of entries to display on the list view
    can_export=True

class Works(db.Model):
    __tablename__ = 'works'
    id = db.Column(db.Integer,primary_key=True)
    work_no=db.Column(db.String(80))
    lot_id=db.Column(db.String(80))
    work_name=db.Column(db.Unicode)
    company=db.Column(db.String(160))
    prod_name=db.Column(db.String(180))
    anod_type=db.Column(db.Unicode)
    person= db.Column(db.String(80))
    person_count=db.Column(db.Integer)
    prod_serial=db.Column(db.String(160))
    in_out=db.Column(db.Unicode)
    pub_time=db.Column(db.DateTime)
    message=db.Column(db.String(180))
    filename=db.Column(db.String(300))
    filelocation=db.Column(db.String(1000))
    data=db.Column(db.BLOB)
    stage= db.Column(db.String(80))
    work_no2= db.Column(db.String(80))
    in_out2= db.Column(db.String(80))
    com_id= db.Column(db.Integer)

    def __repr__(self):
    	return self.id

class Persons(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60))
    username = db.Column(db.String(80), nullable=False,unique=True)
    password=db.Column(db.String(300),nullable=False)
    email = db.Column(db.String(120), unique=True)
    active=db.Column(db.Boolean(),nullable=False)
    confirmed_at=db.Column(db.DateTime())

    def __repr__(self):
        return self.username

class Stage(db.Model):
    __tablename__ = 'stage'
    stage_id=db.Column(db.Integer, primary_key=True)
    id=db.Column(db.Integer)
    work=db.Column(db.String(120))
    zone=db.Column(db.String(120))
    zone_id=db.Column(db.String(100))
    work_code=db.Column(db.String(60))
    def __repr__(self):
        return self.work

class Lot(db.Model):
    __tablename__ = 'lot'
    id = db.Column(db.Integer, primary_key=True)
    lot_id= db.Column(db.String(80))
    com_id=db.Column(db.Integer, db.ForeignKey('company.id'))
    com_name=db.relationship("Company", backref=db.backref('lot'), lazy=True)
    company=db.Column(db.String(160))
    counts=db.Column(db.Integer)
    person= db.Column(db.String(80))
    gen= db.Column(db.String(80))
    prod_type=db.Column(db.Integer, db.ForeignKey('product.prod_id'))
    prod_category= db.Column(db.String(80))
    #prod_category= db.relationship("Product", backref=db.backref('lot'), lazy=True)
    prod_name= db.Column(db.String(180))
    prod_serial= db.Column(db.String(80))
    anod_type= db.Column(db.String(80))
    pol_YN= db.Column(db.String(80))
    mask_YN= db.Column(db.String(80))
    shil_YN= db.Column(db.String(80))
    shil_type= db.Column(db.String(80))
    surf_layer= db.Column(db.String(80))
    RA= db.Column(db.String(80))
    cur_work=db.Column(db.String(80))
    cur_zone=db.Column(db.String(80))
    pre_work=db.Column(db.String(80))   
    pre_zone=db.Column(db.String(80))
    next_work=db.Column(db.String(80))
    next_zone=db.Column(db.String(80))
    cur_progress=db.Column(db.Integer)
    in_date=db.Column(db.DateTime)
    target_date=db.Column(db.DateTime)
    proc1=db.Column(db.String(80))
    proc2=db.Column(db.String(80))
    proc3=db.Column(db.String(80))
    proc4=db.Column(db.String(80))
    proc5=db.Column(db.String(80))
    proc6=db.Column(db.String(80))
    proc7=db.Column(db.String(80))
    proc8=db.Column(db.String(80))
    proc9=db.Column(db.String(80))
    proc10=db.Column(db.String(80))
    proc11=db.Column(db.String(80))
    proc12=db.Column(db.String(80))
    proc13=db.Column(db.String(80))
    proc14=db.Column(db.String(80))
    proc15=db.Column(db.String(80))
    proc16=db.Column(db.String(80))
    proc17=db.Column(db.String(80))
    proc18=db.Column(db.String(80))
    proc19=db.Column(db.String(80))
    proc20=db.Column(db.String(80))
    proc21=db.Column(db.String(80))
    proc22=db.Column(db.String(80))
    proc23=db.Column(db.String(80))
    proc24=db.Column(db.String(80))
    proc25=db.Column(db.String(80))
    proc26=db.Column(db.String(80))
    proc27=db.Column(db.String(80))
    proc28=db.Column(db.String(80))
    proc29=db.Column(db.String(80))
    proc30=db.Column(db.String(80))
    proc31=db.Column(db.String(80))
    proc32=db.Column(db.String(80))
    proc33=db.Column(db.String(80))
    proc34=db.Column(db.String(80))
    proc35=db.Column(db.String(80))
    proc36=db.Column(db.String(80))
    proc37=db.Column(db.String(80))
    proc38=db.Column(db.String(80))
    proc39=db.Column(db.String(80))
    proc40=db.Column(db.String(80))
    proc41=db.Column(db.String(80))
    proc42=db.Column(db.String(80))
    proc43=db.Column(db.String(80))
    proc44=db.Column(db.String(80))
    proc45=db.Column(db.String(80))
   
    def __str__(self):
        return self.lot_id


class Stage_procs(db.Model):
    __tablename__ = 'stage_procs'
    id = db.Column(db.Integer, primary_key=True)
    company=db.Column(db.String(80))
    product= db.Column(db.String(80))
    proc01=db.Column(db.String(80))
    proc02=db.Column(db.String(80))
    proc03=db.Column(db.String(80))
    proc04=db.Column(db.String(80))
    proc05=db.Column(db.String(80))
    proc06=db.Column(db.String(80))
    proc07=db.Column(db.String(80))
    proc08=db.Column(db.String(80))
    proc09=db.Column(db.String(80))
    proc10=db.Column(db.String(80))
    proc11=db.Column(db.String(80))
    proc12=db.Column(db.String(80))
    proc13=db.Column(db.String(80))
    proc14=db.Column(db.String(80))
    proc15=db.Column(db.String(80))
    proc16=db.Column(db.String(80))
    proc17=db.Column(db.String(80))
    proc18=db.Column(db.String(80))
    proc19=db.Column(db.String(80))
    proc20=db.Column(db.String(80))
    proc21=db.Column(db.String(80))
    proc22=db.Column(db.String(80))
    proc23=db.Column(db.String(80))
    proc24=db.Column(db.String(80))
    proc25=db.Column(db.String(80))
        
    def __str__(self):
        return self.product


class Anod(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    anod_type= db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.anod_type

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    com_name= db.Column(db.String(120), nullable=False)
    
    def __str__(self):
        return self.com_name

class Product(db.Model):
    __tablename__ = 'product'
    prod_no = db.Column(db.Integer, primary_key=True)
    prod_name= db.Column(db.String(120), nullable=False)
    prod_id = db.Column(db.Integer)
    def __str__(self):
        return self.prod_name



class Gen(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    prod_gen= db.Column(db.String(80), nullable=False)

    def __str__(self):
        return self.prod_gen


class LotView(ModelView):
    can_set_page_size = True
    can_create = True
    can_delete=False
    create_modal = True
    edit_modal = True
    can_export=True
    can_view_details = True
    export_types = ['xlsx']
    column_searchable_list = ['lot_id', 'prod_name','person' ,'prod_serial','in_date']
    column_export_exclude_list= ['company','cur_work', 'cur_zone','pre_work', 'pre_zone','next_work', 'next_zone','cur_progress','proc1','proc2','proc3',
                                'proc4','proc5','proc6','proc7','proc8','proc9','proc10','proc11','proc12','proc13','proc14','proc15','proc16','proc17','proc18',
                                'proc19','proc20','proc21','proc22','proc23','proc24','proc25','proc26','proc27','proc28','proc29','proc30','proc31','proc32',
                                'proc33','proc34','proc35','proc36','proc37','proc38','proc39','proc40','proc41','proc42','proc43','proc44','proc45']
    column_exclude_list= ['company','cur_work', 'cur_zone','pre_work', 'pre_zone','next_work', 'next_zone','cur_progress','proc1','proc2','proc3',
                                'proc4','proc5','proc6','proc7','proc8','proc9','proc10','proc11','proc12','proc13','proc14','proc15','proc16','proc17','proc18',
                                'proc19','proc20','proc21','proc22','proc23','proc24','proc25','proc26','proc27','proc28','proc29','proc30','proc31','proc32',
                                'proc33','proc34','proc35','proc36','proc37','proc38','proc39','proc40','proc41','proc42','proc43','proc44','proc45']
    column_labels = {'lot_id':'LOT ID', 'com_name': '업체','prod_category': '품목 종류','counts': '수량','person':'담당자','gen': '세대', 
                    'prod_name':'품목', 'prod_serial': '제품 시리얼','anod_type': '아노다이징 종류','pol_YN': '폴리싱 유무',
                    'mask_YN': '마스킹 유무','shil_YN': '실링유무','shil_type': '실링 종류','surf_layer': '막두께',
                    'RA': 'RA','cur_work':'현재 공정', 'cur_zone':'현재 공정위치','pre_work':'이전 공정','pre_zone':'이전 공정위치',
                    'next_work':'다음 공정','next_zone':'다음 공정위치', 'in_date': '입고일','target_date': '납기일'}
    #column_formatters = = dict(company=lambda v, c, m, p: m.com_name) # `view` is current administrative view
    # `context` is instance of jinja2.runtime.Context
    # `model` is model instance
    # `name` is property name
    from datetime import date
    from flask_admin.model import typefmt

    def date_format(view, value):
        return value.strftime('%Y-%m-%d')

    MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
    MY_DEFAULT_FORMATTERS.update({
            type(None): typefmt.null_formatter,
            date: date_format
        })
    
    column_type_formatters = MY_DEFAULT_FORMATTERS

    form_excluded_columns = ['company','cur_work', 'cur_zone','pre_work', 'pre_zone','next_work', 'next_zone','cur_progress','proc1','proc2','proc3',
                                'proc4','proc5','proc6','proc7','proc8','proc9','proc10','proc11','proc12','proc13','proc14','proc15','proc16','proc17','proc18',
                                'proc19','proc20','proc21','proc22','proc23','proc24','proc25','proc26','proc27','proc28','proc29','proc30','proc31','proc32',
                                'proc33','proc34','proc35','proc36','proc37','proc38','proc39','proc40','proc41','proc42','proc43','proc44','proc45']
    form_args = {
            'com_name' :{
                'label':'업체'

            },
            'prod_category': {
                'label': '품목 종류'
            },
            'counts': {
                'label': '수량'
            },
            'person': {
                'label': '담당자'
            },
            'gen': {
                'label': '세대'
            },
            'prod_name': {
                'label': '품목'
            },
            'prod_serial': {
                'label': '제품 시리얼'
            },
            'anod_type': {
                'label': '아노다이징 종류'
            },
            'pol_YN': {
                'label': '폴리싱 유무'
            },
            'mask_YN': {
                'label': '마스킹 유무'
            },
            'shil_YN': {
                'label': '실링유무'
            },
            'shil_type': {
                'label': '실링 종류'
            },
            'surf_layer': {
                'label': '막두께'
            },
            'RA': {
                'label': 'RA'
            },
            'in_date': {
                'label': '입고일'
            },
            'target_date': {
                'label': '납기일'
            }

        }



class WorkView(ModelView):
    column_searchable_list= ['lot_id','company', 'prod_name','person' ,'prod_serial','in_out','pub_time']
    column_export_exclude_list=['filelocation','data','stage','work_no2','in_out2','com_id']
    column_exclude_list=['filelocation','data','stage','work_no2','in_out2','com_id']
    column_labels = { 'work_no':'작업번호','company':  '업체','work_name':'공정','prod_name':  '제품','anod_type':'아노다이징',
                       'person':'작업자','person_count':'작업인원','prod_serial':'제품시리얼번호','in_out':'투입/완료',
                       'pub_time':'입력시간','message':'작업메모','filename': '사진파일'}
    can_create=True
    can_delete=False
    can_export=True
    create_modal=True
    edit_modal=True
    can_view_details=True
    can_set_page_size = True
    export_types = ['xlsx']
    form_excluded_columns=['filelocation','data','stage','work_no2','in_out2','com_id']
    form_args = {
                'work_no': {
                    'label': '작업번호'
                },
                'company': {
                    'label': '업체'
                },
                'work_name':{
                    'label': '공정'
                },
                'prod_name': {
                    'label': '제품'
                },
                'anod_type': {
                    'label': '아노다이징'
                },
                'person': {
                    'label': '작업자'
                },
                'person_count': {
                    'label': '작업인원'
                },
                'prod_serial': {
                    'label': '제품시리얼번호'
                },
                'in_out': {
                    'label': '투입/완료'
                },
                'pub_time': {
                    'label': '입력시간'
                },
                'message': {
                    'label': '작업메모'
                },
                'filename': {
                    'label': '사진파일'
                }
            }


