# -*- coding: utf-8 -*-


from flask_restless import APIManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
import os
from prod_app import app,db, APP_ROOT
from models import LimitModelView,Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen,LotView,WorkView
from sqlalchemy import and_,or_, alias, not_
import sqlite3
import csv
import codecs
import datetime

conn=sqlite3.connect(APP_ROOT+os.sep+'DATABASE.db')
cur=conn.cursor()

def ins_workdata(filename):
    f=codecs.open(APP_ROOT +os.sep+ filename,'r', encoding='euc-kr', errors='ignore')
    data=csv.reader(f)
    for row in data:
        lot_id=row[1]
        company=row[2]
        print(company)
        prod_name=row[3]
        work_name=row[4]
        in_out=row[5]
        try:
            pub_time=datetime.datetime.strptime(row[6], '%Y-%m-%d %H:%M')
        except:
            pub_time=''
        try:
            person_count=int(row[9])
        except:
            person_count=0
        person=row[10]
        prod_serial=row[11]

        lot=Lot.query.filter(Lot.lot_id==lot_id).first()
        print(lot)
        if lot is None:
            com=None
        else:
            com=Company.query.filter(Company.com_name.contains(lot.company)).first()
        if com is None:
            com=Company.query.filter(Company.com_name.contains(company)).first()
            if com is None:
                com_id=""
        else:
            com_id=com.id
        try:
            if prod_name=='':
                prod_name=lot.prod_name
        except:
            prod_name=''

        work=Stage.query.filter(Stage.work==work_name).first()
        if work is None:
            work=Stage.query.filter(Stage.id==988).first()
        stg=work.id
        stage= '%03d' % stg
        zone=work.zone_id
        zone_name=work.zone
        if in_out =='투입' : io = '0'
        else: io = '1'
        work_no_list=[lot_id,'_',stage]
        lot_stage= ''.join(work_no_list)
        try:
            pre_workno=Works.query.filter(Works.work_no2.like(lot_stage + '%')).order_by(Works.work_no2.desc()).first()
        except:
            pre_workno=None
        if pre_workno is None:
            work_no_list.extend(['01','_',io])
        else:
            if str(pre_workno.work_no)[-1:]!= io :
                if io=='1':
                    work_no_list.extend([str(pre_workno.work_no)[-4:-2],'_','1'])
                else:
                    n= int(str(pre_workno.work_no)[-4:-2]) + 1
                    work_no_list.extend([ '%02d' % n,'_','0'])
            else:
                n= int(str(pre_workno.work_no)[-4:-2]) + 1
                work_no_list.extend([ '%02d' % n,'_',io])
        work_no = ''.join(work_no_list)
        work_no2 = work_no[:-2]

        #work=Works(lot_id=lot_id, work_name=work_name, work_no=work_no, work_no2=work_no2, company=company, prod_name=prod_name, stage=stage, com_id=com_id, in_out=in_out, person=person, person_count=person_count, in_out2=io, pub_time=pub_time)
        #db.session.add(work)
        #db.session.commit()
        
        sql = '''insert into works(lot_id,company,prod_name,work_name,work_no,work_no2,stage,com_id,in_out,in_out2,pub_time,
        			person_count,person,prod_serial) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cur.execute(sql,(lot_id,company,prod_name,work_name,work_no,work_no2,stage,com_id,in_out,io,pub_time,person_count,person,prod_serial))
        conn.commit()
        print('Data:', work_no, 'complete.')
    print('Data uploading completed!')
    f.close()

def ins_lotdata(filename):
    file=codecs.open(APP_ROOT +os.sep+ filename,'r', encoding='euc-kr', errors='ignore')
    data=csv.reader(file)
    for row in data:
        in_date=datetime.datetime.strptime(row[1], '%Y-%m-%d')
        lot_id=row[2]
        company=row[3]
        try:
            counts=int(row[4])
        except:
            counts=0
        person=row[5]
        gen=row[6]
        prod_name=row[7]
        anod_type=row[8]
        pol_YN=row[9]
        mask_YN=row[10]
        shil_YN=row[11]
        shil_type=row[12]
        surf_layer=row[13]
        RA=row[14]
        prod_serial=row[15]
        target_date=datetime.datetime.strptime(row[16], '%Y-%m-%d')
        cur_work=row[17]
        try:
            com=Company.query.filter(Company.com_name.contains(company)).first()
            com_id=com.id
        except:
            com_id=""
        try:
            stage=Stage.query.filter(Stage.work==cur_work).first()
        except:
            stage=Stage.query.filter(Stage.zone==cur_work).first()
        if stage is None:
            stage=Stage.query.filter(Stage.id==988).first()
        cur_zone=stage.zone
        
        sql = '''insert into lot(in_date,lot_id,company,counts,person,gen,prod_name,anod_type,pol_YN,mask_YN,shil_YN,shil_type,
                surf_layer,RA,prod_serial,target_date,cur_work,cur_zone,com_id) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cur.execute(sql,(in_date,lot_id,company,counts,person,gen,prod_name,anod_type,pol_YN,mask_YN,shil_YN,shil_type,surf_layer,RA,prod_serial,target_date,cur_work,cur_zone,com_id))
        conn.commit()
        print('Data:', lot_id, 'complete.')
    print('Data uploading completed!')
    file.close()



def update_prodtype():
    compro_list=[{'prod_name': ['LINER','이중월','이중_WALL','WALL_LINER'],'gen':['A3','6G'],'others':0}]
    compro_list.append({'prod_name': ['DRY GAMMA'],'gen':[],'others':0})
    compro_list.append({'prod_name': ['LINER','이중월','이중_WALL','WALL_LINER'],'gen':['A3','6G'],'others':1})
    compro_list.append({'prod_name':['DIFFUSER','D/F'],'gen':['A3','6G'],'others':0})
    compro_list.append({'prod_name':['DIFFUSER','D/F'],'gen':['A2','5.5G'],'others':0})
    compro_list.append({'prod_name':['DIFFUSER','D/F'],'gen':['A3','6G','A2','5.5G'],'others':1})
    compro_list.append({'prod_name':['SUSCEPTOR','S/T'],'gen':['A3','6G'],'others':0})
    compro_list.append({'prod_name':['SUSCEPTOR','S/T'],'gen':['A2','5.5G'],'others':0})
    compro_list.append({'prod_name':['SUSCEPTOR','S/T'],'gen':['A3','6G','A2','5.5G'],'others':1})
    compro_list.append({'prod_name':['SHADOW_FRAME','SHADOWFRAME','S/F'],'gen':['A3','6G'],'others':0})
    compro_list.append({'prod_name':['SHADOW_FRAME','SHADOWFRAME','S/F'],'gen':['A2','5.5G'],'others':0})
    compro_list.append({'prod_name':['SHADOW_FRAME','SHADOWFRAME','S/F'],'gen':['A3','6G','A2','5.5G'],'others':1})
    compro_list.append({'prod_name':['하부전극'],'gen':[],'others':0})
    compro_list.append({'prod_name': ['TRAY_PLATE'],'gen':[],'others':0})
    compro_list.append({'prod_name': ['SHOWER_HEAD'],'gen':[],'others':0})
    compro_list.append({'prod_name': ['RWD'],'gen':[],'others':0})
    compro_list.append({'prod_name': ['SCE'],'gen':[],'others':0})
    
    
   
    cur.execute("update lot set prod_category ='기타_제품' ")
    conn.commit()
    
    lot=Lot.query.subquery()
    dt_lot=[]
    for compro in compro_list:
        if compro['others']==0 :
            sublot=lot
            try:
                com_prod=compro['gen'][0]
            except:
                com_prod=''
            if compro['gen']!=[]:
                gens=[]
                for gen in compro['gen']:
                    gens.append(sublot.c.gen.contains(gen))
                sublot = db.session.query(sublot).filter(or_(*gens)).subquery()
            prods = []
            for name in compro['prod_name']:
                prods.append(sublot.c.prod_name.contains(name))
            sublot = db.session.query(sublot).filter(or_(*prods)).subquery()
            if compro['gen']==[]:
                com_prod+='' + compro['prod_name'][0].replace(' ','_')
            else:
                com_prod+='_' + compro['prod_name'][0].replace(' ','_')

            lot_work=db.session.query(sublot).all()
            lot_cnt=db.session.query(sublot).count()
            dt_lot.append({'prod':com_prod,'lot_id':[r.lot_id for r in lot_work],'count':lot_cnt})

    
        elif compro['others']==1:
            otherlot=lot
            prods = []
            for name in compro['prod_name']:
                prods.append(otherlot.c.prod_name.contains(name))
            sublot = db.session.query(otherlot).filter(or_(*prods)).subquery()
            gens=[]
            for gen in compro['gen']:
                gens.append(~sublot.c.gen.contains(gen))
            sublot = db.session.query(sublot).filter(and_(*gens)).subquery()

            lot_work=db.session.query(sublot).all()
            com_prod= compro['prod_name'][0] + '_기타'
            
            dt_lot.append({'prod':com_prod,'lot_id':[r.lot_id for r in lot_work]})
        else: 
            otherlot2=lot
            prods = []
            for name in compro['prod_name']:
                prods.append(~otherlot2.c.prod_name.contains(name))
            sublot = db.session.query(otherlot2).filter(and_(*prods)).subquery()

            lot_work=db.session.query(sublot).all()
            com_prod='기타_제품'
            dt_lot.append({'prod':com_prod,'lot_id':[r.lot_id for r in lot_work]})

   
    return dt_lot


def update_lot_prod(lot_id,prod_cat):
    try:
        sql='update lot set prod_category =? where lot_id=?'
        cur.execute(sql,(prod_cat,lot_id))
        conn.commit()
        print('Lot ID:', lot_id,'Product', prod_cat, 'complete.')
        
    
        return 1
    except:
        return 0
