# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
from flask_socketio import SocketIO, send, emit
from sqlalchemy import and_,or_, alias, not_
import json
import os
import datetime
from dateutil.parser import parse
from prod_app import app,db
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen



socketio=SocketIO(app)



@socketio.on( 'event' )
def handle_custom_event( jsonmsg ):
    #handle_my_custom_event
  #print( 'recived my event: ' + str( jsonmsg ) )
    pub_timeserial=datetime.datetime.now()
    pub_time=pub_timeserial.strftime('%Y-%m-%d @ %H:%M:%S')
    json_encoded=json.dumps(jsonmsg)
    json_data=json.loads(json_encoded)
    lot_id=json_data['lot_id']
    lot=Lot.query.filter(Lot.lot_id==lot_id).first()
    if lot=='' or lot is None:
        return '<script> window.alert("lot정보가 존재하지 않습니다.")</script>'
    else:

        com=Company.query.filter(Company.com_name==lot.company).first()
        if com is None:
            com=Company.query.filter(Company.com_name.contains(lot.company)).first()
        com_id=int(com.id)
        message=json_data['message']

        if json_data['work_name']:
            work_name=json_data['work_name']
            work=Stage.query.filter(Stage.work==work_name).first()
            stg=work.id
            stage= '%03d' % stg
        elif json_data['stage']:
            stg=int(json_data['stage'])
            stage= '%03d' % stg
            work=Stage.query.filter(Stage.id==stage).first()
            work_name=work.work
        zone=work.zone_id
        zone_name=work.zone
        in_out=json_data['in_out']
        if in_out =='투입' : io = '0'
        else: io = '1'
        alert=''
        person=json_data['person']
        person_count=int(json_data['person_count']) 
        if json_data['filename']!='':
            jsonmsg['pub_time']=pub_time
            jsonmsg['company']=lot.company
            jsonmsg['prod_name']=lot.prod_name
            jsonmsg['zone']=zone
            alert='사진이 업로드되었습니다.'
            if alert!='':
                jsonmsg['alert']=alert
            print(jsonmsg)
            socketio.emit( 'response', jsonmsg, broadcast=True)
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

            jsonmsg['pub_time']=pub_time
            jsonmsg['company']=lot.company
            jsonmsg['prod_name']=lot.prod_name
            jsonmsg['id']=work_id.id
            jsonmsg['zone']=zone

            if alert!='':
                jsonmsg['alert']=alert
            print(jsonmsg)
            socketio.emit( 'response', jsonmsg, broadcast=True)
