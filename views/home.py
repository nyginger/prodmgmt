# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
from sqlalchemy import and_,or_, alias, not_
import json
import os
import datetime
from dateutil.parser import parse
from eins_app import app,db, APP_ROOT, query_db,cur,conn
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen
import sqlite3


#@app.route( '/' , methods=['GET','POST'])
#@login_required
#def index():

#    stages=Stage.query.order_by(Stage.id.asc()).all()
#    return render_template( 'index2.html', stages=stages)

@app.route('/')
def home():
    
    com_list=['SDC','LG','삼성반도체','원익IPS']
    compro_list=[]
    dt_in=[]
    dt_work=[]
    lot=Lot.query.filter(and_((Lot.cur_work!="출고처리"),or_((Lot.next_work==""),(Lot.next_work!="출고처리")))).subquery()
    
    for com in com_list:
        sublot=db.session.query(lot).filter(lot.c.company.contains(com)).subquery()
        results=cur.execute("select prod_category from lot where company=?", [com])
        conn.commit()
        prod_list=results.fetchall()
        prod_list =list(set(prod_list))
        for prod in prod_list:
            com_prod=com+'_'+prod[0]
            print(com_prod)
            comprod_lot=db.session.query(sublot).filter(sublot.c.prod_category==prod[0]).subquery()
            lot_work=db.session.query(comprod_lot).all()
            lot_work_cnt=db.session.query(comprod_lot).count()
            if lot_work_cnt>0:
                dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
    
    other = []
    for name in com_list:
        other.append(not_(lot.c.company.contains(name)))
    sublot = db.session.query(lot).filter(and_(*other)).subquery()
    lot_work=db.session.query(sublot).order_by(sublot.c.lot_id.desc()).all()
    lot_work_cnt=db.session.query(sublot).count()
    com_prod='기타 업체'
    
    dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})

    return render_template( 'home.html',dt_work=dt_work,dt_in=dt_in, compro_list=compro_list)





def home2():

    compro_list=[{'name':'SDC','prod_name': ['LINER','이중월','이중_WALL','WALL_LINER'],'gen':['A3','6G'],'others':0}]
    compro_list.append({'name':'SDC','prod_name': ['LINER','이중월','이중_WALL','WALL_LINER'],'gen':['A3','6G'],'others':1})
    compro_list.append({'name':'SDC','prod_name':['DIFFUSER','D/F'],'gen':['A3','6G'],'others':0})
    compro_list.append({'name':'SDC','prod_name':['DIFFUSER','D/F'],'gen':['A2','5.5G'],'others':0})
    compro_list.append({'name':'SDC','prod_name':['DIFFUSER','D/F'],'gen':['A3','6G','A2','5.5G'],'others':1})
    compro_list.append({'name':'SDC','prod_name':['SUSCEPTOR','S/T'],'gen':['A3','6G'],'others':0})
    compro_list.append({'name':'SDC','prod_name':['SUSCEPTOR','S/T'],'gen':['A2','5.5G'],'others':0})
    compro_list.append({'name':'SDC','prod_name':['SUSCEPTOR','S/T'],'gen':['A3','6G','A2','5.5G'],'others':1})
    compro_list.append({'name':'SDC','prod_name':['SHADOW_FRAME','SHADOWFRAME','S/F'],'gen':['A3','6G'],'others':0})
    compro_list.append({'name':'SDC','prod_name':['SHADOW_FRAME','SHADOWFRAME','S/F'],'gen':['A2','5.5G'],'others':0})
    compro_list.append({'name':'SDC','prod_name':['SHADOW_FRAME','SHADOWFRAME','S/F'],'gen':['A3','6G','A2','5.5G'],'others':1})
    compro_list.append({'name':'SDC','prod_name':['하부전극'],'gen':[],'others':0})
    compro_list.append({'name':'SDC','prod_name':['LINER','이중월','이중_WALL','DIFFUSER','D/F','SUSCEPTOR','S/T','하부전극','SHADOW_FRAME','S/F'],'gen':[],'others':2})
    compro_list.append({'name':'LG','prod_name': ['TRAY_PLATE'],'gen':[],'others':0})
    compro_list.append({'name':'LG','prod_name': ['SHOWER_HEAD'],'gen':[],'others':0})
    compro_list.append({'name':'LG','prod_name': ['TRAY_PLATE','SHOWER_HEAD'],'gen':[],'others':2})
    compro_list.append({'name':'삼성반도체','prod_name': ['RWD'],'gen':[],'others':0})
    compro_list.append({'name':'삼성반도체','prod_name': ['SCE'],'gen':[],'others':0})
    compro_list.append({'name':'삼성반도체','prod_name': ['RWD','SCE'],'gen':[],'others':2})
    compro_list.append({'name':['SDC','LG','삼성반도체'],'others':3})
    lot=Lot.query.filter(and_((Lot.cur_work!="출고처리"),or_((Lot.next_work==""),(Lot.next_work!="출고처리")))).subquery()
    dt_in=[]
    dt_work=[]
    
    for compro in compro_list:
        if compro['others']==0 :
            sublot=db.session.query(lot).filter(lot.c.company.contains(compro['name'])).subquery()
            sublot_cnt=db.session.query(sublot).count()
            com_prod=compro['name']
            if compro['gen']!=[]:
                com_prod+=' ' + compro['gen'][0]
                gens=[]
                for gen in compro['gen']:
                    gens.append(sublot.c.gen.contains(gen))
                sublot = db.session.query(sublot).filter(or_(*gens)).subquery()
            prods = []
            for name in compro['prod_name']:
                prods.append(sublot.c.prod_name.contains(name))
            sublot = db.session.query(sublot).filter(or_(*prods)).subquery()
            com_prod+=' ' + compro['prod_name'][0]
            sub_in=db.session.query(sublot).filter(sublot.c.cur_work=='입고처리').subquery()
            sub_work=db.session.query(sublot).filter(sublot.c.cur_work!='입고처리').subquery()
            lot_in=db.session.query(sub_in).order_by(sub_in.c.lot_id.desc()).all()
            lot_in_cnt=db.session.query(sub_in).count()
            lot_work=db.session.query(sub_work).order_by(sub_work.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sub_work).count()
            dt_in.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_in],'count':lot_in_cnt})
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
        elif compro['others']==1:
            otherlot=db.session.query(lot).filter(lot.c.company.contains(compro['name'])).subquery()
            prods = []
            for name in compro['prod_name']:
                prods.append(otherlot.c.prod_name.contains(name))
            sublot = db.session.query(otherlot).filter(or_(*prods)).subquery()
            gens=[]
            for gen in compro['gen']:
                gens.append(~sublot.c.gen.contains(gen))
            sublot = db.session.query(sublot).filter(and_(*gens)).subquery()
            sub_in=db.session.query(sublot).filter(sublot.c.cur_work=='입고처리').subquery()
            sub_work=db.session.query(sublot).filter(sublot.c.cur_work!='입고처리').subquery()
            lot_in=db.session.query(sub_in).order_by(sub_in.c.lot_id.desc()).all()
            lot_in_cnt=db.session.query(sub_in).count()
            lot_work=db.session.query(sub_work).order_by(sub_work.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sub_work).count()
            com_prod=compro['name'] + ' ' + compro['prod_name'][0] + ' 기타'
            dt_in.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_in],'count':lot_in_cnt})
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
        elif compro['others']==2:
            otherlot2=db.session.query(lot).filter(lot.c.company.contains(compro['name'])).subquery()
            prods = []
            for name in compro['prod_name']:
                prods.append(~otherlot2.c.prod_name.contains(name))
            sublot = db.session.query(otherlot2).filter(and_(*prods)).subquery()
            sub_in=db.session.query(sublot).filter(sublot.c.cur_work=='입고처리').subquery()
            sub_work=db.session.query(sublot).filter(sublot.c.cur_work!='입고처리').subquery()
            lot_in=db.session.query(sub_in).order_by(sub_in.c.lot_id.desc()).all()
            lot_in_cnt=db.session.query(sub_in).count()
            lot_work=db.session.query(sub_work).order_by(sub_work.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sub_work).count()
            com_prod=compro['name'] + ' 기타'
            dt_in.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_in],'count':lot_in_cnt})
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
        else:
            other = []
            for name in compro['name']:
                other.append(not_(lot.c.company.contains(name)))
            sublot = db.session.query(lot).filter(and_(*other)).subquery()
            sub_in=db.session.query(sublot).filter(sublot.c.cur_work=='입고처리').subquery()
            sub_work=db.session.query(sublot).filter(sublot.c.cur_work!='입고처리').subquery()
            lot_in=db.session.query(sub_in).order_by(sub_in.c.lot_id.desc()).all()
            lot_in_cnt=db.session.query(sub_in).count()
            lot_work=db.session.query(sub_work).order_by(sub_work.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sub_work).count()
            com_prod='기타 업체'
            dt_in.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_in],'count':lot_in_cnt})
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
    return render_template( 'home.html',dt_work=dt_work,dt_in=dt_in, compro_list=compro_list)


@app.route('/prod', methods=['GET', 'POST'])
def prod():
    if request.method=='GET':
        
        prod=request.args.get('prod')
        com=prod.split(' ')[0]

        lot_list=request.args.getlist('lot_list')

    else:
        prod=request.form['prod']
        com=prod.split(' ')[0]
        lot_list=request.form.getlist('lot_list')
        
        dt_in=request.form.getlist('dt_in')
        dt_work=request.form.getlist('dt_work')
        
        
    #print(dt_work)
   
    #json_data=json.loads(json_encoded)
  
    dt=[] 
    if com!='기타':
        lot=Lot.query.filter(Lot.lot_id.in_(lot_list)).subquery()
        try:
            zone=request.form['zone']
            print(zone)
            zone_id=request.form['zone_id']
            z_works=Stage.query.filter(Stage.zone_id==zone_id).all()
            print(z_works)
            work_list=[]
            for zw in z_works:
                sublot=db.session.query(lot).filter(lot.c.cur_work.contains(zw.work)).all()
                dt.append({'work':zw.work, 'lot_id':[r.lot_id for r in sublot]})
                work_list.append(~lot.c.cur_work.contains(zw.work))
            sublot = db.session.query(lot).filter(and_(*work_list)).all()
            dt.append({'work':zone, 'lot_id':[r.lot_id for r in sublot]})
        except:
            
            for i in range(1,10):
                if i != 8 :
                    zone=Stage.query.filter(Stage.zone_id==i).first()
                    sublot=db.session.query(lot).filter(lot.c.cur_zone.contains(str(zone.zone))).all()
                    dt.append({'zone':zone.zone, 'lot_id':[r.lot_id for r in sublot]})
        print(dt)

        return jsonify({'dt':dt, 'prod':prod})
    else:

        slot=Lot.query.filter(Lot.lot_id.in_(lot_list)).order_by(Lot.company.asc()).subquery()
        lot=db.session.query(slot).all()
         
        zone=['입고','폴리싱','마스킹','아노다이징','출고','소형CR','외주','생산관리']
        comp=[]
        for l in lot:
            if l.company not in comp:
                comp.append(l.company)
        for co in comp:
            com_dt={'company':'','1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'9':[]}
            com_dt['company']=co
            dt.append(com_dt)
        for l in lot:
            x=0
            y=0
            for i in range(0,len(comp)):
                if l.company==comp[i]:
                    x=i 
            for z in zone:
                if l.cur_zone==z:
                    stage=Stage.query.filter(Stage.zone==z).first()
                    y=stage.zone_id
            if y>0:
                dt[x][str(y)].append(l.lot_id)
        print(dt)
        return render_template( 'prod_page.html', dt=dt, prod=prod,zone=zone)



