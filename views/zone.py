# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
from sqlalchemy import and_,or_, alias, not_
import json
import os
import datetime
from dateutil.parser import parse
from eins_app import app,db,APP_ROOT, cur, conn
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen

from pusher import Pusher

pusher = Pusher(
    app_id = "501801",
    key = "f62b267e5d5448667b8a",
    secret = "a7c03740e706cec3fdc4",
    cluster = "ap1"
)


@app.route( '/zonepage' , methods=['GET','POST'])
#@login_required
def zonepage():
    zone_id=request.args.get('zone_id')
    stages=Stage.query.filter(Stage.zone_id==zone_id).order_by(Stage.id.asc()).all()
    return render_template( 'zonepage.html', stages=stages,zone_id=zone_id)


@app.route('/zone/<int:zone_id>/', defaults={'page': 1}, methods=['GET','POST'])
@app.route('/zone/<int:zone_id>/<int:page>', methods=['GET','POST'])
def zone(zone_id,page):
    stages=Stage.query.all()
    if zone_id==0:
        works=Works.query.order_by(Works.pub_time.desc()).paginate(page,60)
        zone={'zone':'전체공정','zone_id':0}
    else:
        zone=Stage.query.filter(Stage.zone_id==zone_id).first()
        #works=Works.query.join(Stage, Works.work_name==Stage.work).\
        #      add_columns(Works.id,Works.lot_id,Works.work_name,Works.prod_name,Works.company,Works.in_out,Works.person,Stage.zone,Works.pub_time,Works.filename,Works.filelocation).\
        #      filter(Stage.zone_id==zone_id).order_by(Works.pub_time.desc()).paginate(page,10)
        works=Works.query.filter(Works.stage.like(str(zone_id) + '%')).order_by(Works.pub_time.desc()).paginate(page,20)
        
        img_zone=Works.query.filter(Works.stage.like(str(zone_id) + '%'),  Works.filename!='').order_by(Works.pub_time.desc())
        #img_zone=Works.query.join(Stage, Works.work_name==Stage.work).\
        #      add_columns(Works.id,Works.lot_id,Works.work_name,Works.prod_name,Works.company,Works.in_out,Stage.zone,Works.pub_time,Works.filename,Works.filelocation).\
        #      filter((Stage.zone_id==zone_id)&(Works.filename!='')).order_by(Works.pub_time.desc()).paginate(page,10)
 
        img_stg=[]
        for work in img_zone:
            try:
                image_names=os.listdir(os.path.join(APP_ROOT, 'thumbnail', work.lot_id  ))
                for img in image_names:
                    fileinfo=img.split('_')
                    n='%s' % fileinfo[2][:1]
                    if zone_id==int(n):
                        img_stg.append(img)
            except:
                pass
            img_stg=list(set(img_stg))
            print(img_stg)
        return render_template( 'work.html', works=works, idx='works', query='', zone=zone,stages=stages,
                                img_stg=img_stg,img_zone=img_zone)   
    if not works and page != 1:
        abort(404)
    return render_template( 'work.html', works=works, idx='works', query='', zone=zone,stages=stages,
                            img_stg='',img_zone='')



@app.route('/zone_home/<int:zone_id>/',methods=['GET'])
def zone_home(zone_id):
    com_list=['SDC','LG','삼성반도체','원익IPS']

    compro_list=[]
    dt_in=[]
    dt_work=[]
    lot=Lot.query.filter((Lot.cur_work!="출고처리"),(Lot.next_work!="출고처리")).subquery()
    stage=Stage.query.filter(Stage.zone_id==zone_id).first()
    lot_in_work=db.session.query(lot).filter(lot.c.cur_zone==stage.zone).subquery()
    for com in com_list:
        sublot=db.session.query(lot_in_work).filter(lot_in_work.c.company.contains(com)).subquery()
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
        other.append(not_(lot_in_work.c.company.contains(name)))
    sublot = db.session.query(lot_in_work).filter(and_(*other)).subquery()
    lot_work=db.session.query(sublot).order_by(sublot.c.lot_id.desc()).all()
    lot_work_cnt=db.session.query(sublot).count()
    com_prod='기타 업체'
    dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})

    return render_template( 'zone_work.html',dt_work=dt_work,dt_in=dt_in, compro_list=compro_list, zone_id=zone_id,zone=stage.zone)











def zone_home2(zone_id):

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
    lot=Lot.query.filter((Lot.cur_work!="출고처리")).subquery()
    dt_in=[]
    dt_work=[]
    stage=Stage.query.filter(Stage.zone_id==zone_id).first()
    print(stage.zone)
    lot_in_work=db.session.query(lot).filter(lot.c.cur_zone==stage.zone).subquery()
    for compro in compro_list:
        if compro['others']==0 :
            sublot=db.session.query(lot_in_work).filter(lot_in_work.c.company.like(compro['name'] + '%')).subquery()
            sublot_cnt=db.session.query(sublot).count()
            com_prod=compro['name']
            if compro['gen']!=[]:
                com_prod+=' ' + compro['gen'][0]
                gens=[]
                for gen in compro['gen']:
                    gens.append(sublot.c.gen.like(gen))
                sublot = db.session.query(sublot).filter(or_(*gens)).subquery()
            prods = []
            for name in compro['prod_name']:
                prods.append(sublot.c.prod_name.like('%' + name + '%'))
            sublot = db.session.query(sublot).filter(or_(*prods)).subquery()
            com_prod+=' ' + compro['prod_name'][0]
            lot_work=db.session.query(sublot).order_by(sublot.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sublot).count()
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
        elif compro['others']==1:
            otherlot=db.session.query(lot_in_work).filter(lot_in_work.c.company.contains(compro['name'])).subquery()
            prods = []
            for name in compro['prod_name']:
                prods.append(otherlot.c.prod_name.like('%' + name + '%'))
            sublot = db.session.query(otherlot).filter(or_(*prods)).subquery()
            gens=[]
            for gen in compro['gen']:
                gens.append(~sublot.c.gen.like(gen))
            sublot = db.session.query(sublot).filter(and_(*gens)).subquery()
            lot_work=db.session.query(sublot).order_by(sublot.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sublot).count()
            com_prod=compro['name'] + ' ' + compro['prod_name'][0] + ' 기타'
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
        
        elif compro['others']==2:
            otherlot2=db.session.query(lot_in_work).filter(lot_in_work.c.company.contains(compro['name'])).subquery()
            prods = []
            for name in compro['prod_name']:
                prods.append(not_(otherlot2.c.prod_name.like('%' + name + '%')))
            sublot = db.session.query(otherlot2).filter(and_(*prods)).subquery()
            lot_work=db.session.query(sublot).order_by(sublot.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sublot).count()         
            com_prod=compro['name'] + ' 기타'
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
        else:
            other = []
            for name in compro['name']:
                other.append(not_(lot_in_work.c.company.like(name + '%')))
            sublot = db.session.query(lot_in_work).filter(and_(*other)).subquery()
            lot_work=db.session.query(sublot).order_by(sublot.c.lot_id.desc()).all()
            lot_work_cnt=db.session.query(sublot).count()
            com_prod='기타 업체'
   
            dt_work.append({'name':com_prod, 'lot_id':[r.lot_id for r in lot_work],'count':lot_work_cnt})
        print(dt_work)
    return render_template( 'zone_work.html',dt_work=dt_work,dt_in=dt_in, compro_list=compro_list, zone_id=zone_id,zone=stage.zone)




@app.route('/add_zonework', methods=['POST'])
def add_zonework():

    pub_timeserial=datetime.datetime.now()
    pub_time=pub_timeserial.strftime('%Y-%m-%d @ %H:%M:%S')
    '''json_encoded=json.dumps(jsonmsg)
    json_data=json.loads(json_encoded)
    lot_id=json_data['lot_id']'''
    lot_id=request.form.get('lot_id')
    lot=Lot.query.filter(Lot.lot_id==lot_id).first()
    if lot=='' or lot is None:
        return '<script> window.alert("lot정보가 존재하지 않습니다.")</script>'
    else:

        com=Company.query.filter(Company.com_name==lot.company).first()
        if com is None:
            com=Company.query.filter(Company.com_name.contains(lot.company)).first()
        com_id=int(com.id)
        message=request.form.get('message')

        if request.form.get('work_name'):
            work_name=request.form.get('work_name')
            work=Stage.query.filter(Stage.work==work_name).first()
            stg=work.id
            stage= '%03d' % stg
        elif request.form.get('stage'):
            stg=int(request.form.get('stage'))
            stage= '%03d' % stg
            work=Stage.query.filter(Stage.id==stage).first()
            work_name=work.work
        zone=work.zone_id
        zone_name=work.zone
        in_out=request.form.get('in_out')
        if in_out =='투입' : io = '0'
        else: io = '1'
        alert=''
        person=request.form.get('person')
        person_count=int(request.form.get('person_count')) 
        if request.form.get('filename')!='':
            
            pusher.trigger(u'my-channel', u'my-event', {u'message': u'hello world'})
            return jsonify({'result':'사진파일 입력'})
        else:

            work_no_list=[lot_id,'_',stage]
            lot_stage= ''.join(work_no_list)
            #pre_work=Works.query.filter(Works.work_no.like(lot_stage + '%')).order_by(Works.pub_time.desc()).first()
            pre_workno=Works.query.filter(Works.work_no2.like(lot_stage + '%')).order_by(Works.work_no2.desc()).first()
            if pre_workno is None:
                work_no_list.extend(['01','_',io])
                if io=='1':
                    alert= alert + '(투입 이력이 없이, 완료이력만 입력되었습니다.\n투입이력은 수동으로 입력하여 주십시오.)'
            else:
                if str(pre_workno.work_no)[-1:]!= io :
                    if io=='1':
                        work_no_list.extend([str(pre_workno.work_no)[-4:-2],'_','1'])
                    else:
                        n= int(str(pre_workno.work_no)[-4:-2]) + 1
                        work_no_list.extend([ '%02d' % n,'_','0'])
                else:
                    alert=alert + '이전 완료/투입 이력이 없이, 현재이력만 입력되었습니다.\n이전 이력은 수동으로 입력하여 주십시오.'
                    n= int(str(pre_workno.work_no)[-4:-2]) + 1
                    work_no_list.extend([ '%02d' % n,'_',io])
            work_no = ''.join(work_no_list)
            work_no2 = work_no[:-2]
            pub_time=pub_timeserial.strftime('%Y%m%d%H%M%S')   
            work=Works(lot_id=lot_id, work_name=work_name, work_no=work_no, work_no2=work_no2, company=lot.company, prod_name=lot.prod_name, stage=stage, com_id=com_id, in_out=in_out, person=person, person_count=person_count, in_out2=io, pub_time=pub_timeserial,)
            db.session.add(work)
            db.session.commit()
            db.session.query(Lot).filter(Lot.lot_id==lot_id).update({Lot.cur_work:work_name, Lot.cur_zone:zone_name})
            db.session.commit()
            work_id=Works.query.filter(Works.work_no==work_no).first()

            pusher.trigger(u'my-channel', u'my-event', {u'message': u'hello world'})

            return render_template('')