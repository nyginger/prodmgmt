# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
from sqlalchemy import and_,or_, alias, not_
import json
import os
import datetime
from dateutil.parser import parse
from eins_app import app,db,APP_ROOT
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen


@app.route('/create_lot', methods=['POST'])
def create_lot():
    lot_id=request.form['lot_id']
    
    chklot=Lot.query.filter(Lot.lot_id==lot_id).first()
    if chklot:
        return jsonify(error='Lot 존재')
    else:
        company=request.form['com'].upper()
        prod_name=request.form['prod_name']
        prod_name=prod_name.replace(' ','_').upper()
        counts=int(request.form['counts'])
        person=request.form['person']
        gen=request.form['gen']
        anod_type=request.form['anod_type']
        prod_serial=request.form['prod_serial'].upper()
        pol_YN=request.form['pol_YN']
        mask_YN=request.form['mask_YN']
        shil_YN=request.form['shil_YN']
        shil_type=request.form['shil_type']
        surf_layer=request.form['surf_layer']
        ra=request.form['RA']
        in_date=datetime.datetime.now()
        target_date=parse(request.form['target_date']).date()
        com_id=int(request.form['com_id'])
        prod_type=int(request.form['prod_id'])
   
        lot=Lot(lot_id=lot_id, company=company, prod_name=prod_name, counts=counts, person=person, gen=gen, anod_type=anod_type, prod_serial=prod_serial, pol_YN=pol_YN, mask_YN=mask_YN, shil_YN=shil_YN, shil_type=shil_type,surf_layer=surf_layer, RA=ra, in_date=in_date, target_date=target_date, com_id=com_id, prod_type=prod_type, cur_work='입고처리', cur_zone='생산관리')
        db.session.add(lot)
        db.session.commit()
        return jsonify(result='Lot이 등록되었습니다.')




@app.route('/update_lot', methods=['POST'])
def update_lot():
    lot_id=request.form['lot_id']
    company=request.form['com'].upper()
    prod_name=request.form['prod_name']
    prod_name=prod_name.replace(' ','_').upper()
    counts=int(request.form['counts'])
    person=request.form['person']
    gen=request.form['gen']
    anod_type=request.form['anod_type']
    prod_serial=request.form['prod_serial'].upper()
    pol_YN=request.form['pol_YN']
    mask_YN=request.form['mask_YN']
    shil_YN=request.form['shil_YN']
    shil_type=request.form['shil_type']
    surf_layer=request.form['surf_layer']
    ra=request.form['RA']
    in_date=datetime.datetime.now()
    target_date=parse(request.form['target_date']).date()
    com_id=int(request.form['com_id'])
    prod_type=int(request.form['prod_id'])

    db.session.query(Lot).filter(Lot.lot_id==lot_id).update({Lot.company:company, Lot.prod_name:prod_name, Lot.counts:counts, Lot.person:person, Lot.gen:gen, Lot.anod_type:anod_type, Lot.prod_serial:prod_serial, Lot.pol_YN:pol_YN, Lot.mask_YN:mask_YN, Lot.shil_YN:shil_YN, Lot.shil_type:shil_type,Lot.surf_layer:surf_layer, Lot.RA:ra, Lot.target_date:target_date, Lot.com_id:com_id, Lot.prod_type:prod_type })
    db.session.commit()
    return jsonify(result='Lot이 수정되었습니다.')




@app.route('/load_lotinfo')
def load_lotinfo():
    stage_procs=Stage_procs.query.order_by(Stage_procs.company.asc()).all()
    stages=Stage.query.order_by(Stage.id.asc()).all()
    com_list=Company.query.order_by(Company.com_name.asc()).all()
    product=Product.query.order_by(Product.prod_id.asc()).all()
    anod=Anod.query.order_by(Anod.id.asc()).all()
    if request.args.get('lot_id'):
        lot_id=request.args.get('lot_id').upper()
        lot=Lot.query.filter(Lot.lot_id==lot_id).first()
        try:
            sqlstring='select '
            for n in range(1,46):
                sqlstring += ' proc' + str(n) + ','
            sqlstring = sqlstring[:-1] + " from lot where lot_id ='" + lot_id + "'"
            result=db.engine.execute(sqlstring)
            lotprocs=[]
            for row in result:
                lotprocs.append(row)
        except:
            pass
        return render_template('loadlot.html', lot=lot, stage_procs=stage_procs,stages=stages,com_list=com_list,product=product,lotprocs=lotprocs[0], anod=anod)
    else:
        return render_template('loadlot.html', lot=None, stage_procs=stage_procs,stages=stages,com_list=com_list,product=product, anod=anod)



@app.route('/lot_info', methods=['GET'])
def lot_info():
    lot_id=request.args.get('lot_id').upper()
    lot=Lot.query.filter(Lot.lot_id==lot_id).first()
    if lot==None:
        return '<script>alert("Lot 정보 없음")</script>'
    else:
        sqlstring='select '
        for n in range(1,46):
            sqlstring += ' proc' + str(n) + ','
        sqlstring = sqlstring[:-1] + " from lot where lot_id ='" + lot_id + "'"
        result=db.engine.execute(sqlstring)
        lotprocs=[]
        for row in result:
            lotprocs.append(row)
        print(lotprocs)
        try:
            works=Works.query.filter((Works.lot_id==lot_id)&(Works.work_no!='')).order_by(Works.pub_time.desc()).all()
        except:
            works=Works.query.filter((Works.lot_id==lot_id)&(Works.work_no!='')&(Works.pub_time!='')).order_by(Works.pub_time.desc()).all()
        if works==None:
            flash('작업정보 없음')
        stages=Stage.query.all()
        stage_procs=Stage_procs.query.all()
        com_list=Company.query.all()
        try:
            image_names=os.listdir(os.path.join(APP_ROOT, 'thumbnail' , lot_id ) )
            img_stg={}
            for i in range(1,10):
                img_stg['%d' % i]=[]
            for img in image_names:
                filename,file_ext =os.path.splitext(img)
                if file_ext=='.jpg' or file_ext=='.png' or file_ext=='.gif':
                    fileinfo=img.split('_')
                    n='%s' % fileinfo[2][:1]
                    img_stg[n].append(img)

            return render_template("lot_info.html", lot=lot, works=works,stages=stages,
                                    img_stg1=img_stg['1'], img_stg2=img_stg['2'],
                                    img_stg3=img_stg['3'], img_stg4=img_stg['4'],
                                    img_stg5=img_stg['5'], img_stg9=img_stg['9'],
                                    img_stg6=img_stg['6'], img_stg7=img_stg['7'],
                                    lotprocs=lotprocs[0], stage_procs=stage_procs,
                                    com_list=com_list
                                    )
        except:
            return render_template("lot_info.html", lot=lot,works=works,stages=stages,
                                    com_litst=com_list, stage_procs=stage_procs,
                                    lotprocs=lotprocs[0],  image_names='')




@app.route('/lot_rework', methods=['POST'])
def lot_rework():
    json_encoded=request.data.decode("utf-8")
    json_data=json.loads(json_encoded)
    lot_id=json_data['lot_id']
    lot_re_code=json_data['lot_re_code']
    if lot_id[-3:-1]==lot_re_code.upper() :
        lot_re_count=int(lot_id[-1:])
        lot_re_count+=1
        new_lot_id=lot_id[:-1] + str(lot_re_count)
    else:
        new_lot_id=lot_id + '-' + lot_re_code.upper() +'1'
    lot=Lot.query.filter(Lot.lot_id==lot_id).first()
    issue_code=lot_re_code.upper()+'재발행'
    lot1=Lot(lot_id=new_lot_id, company=lot.company, prod_name=lot.prod_name, counts=lot.counts, person=lot.person, gen=lot.gen, anod_type=lot.anod_type, prod_serial=lot.prod_serial, pol_YN=lot.pol_YN, mask_YN=lot.mask_YN, shil_YN=lot.shil_YN, shil_type=lot.shil_type,surf_layer=lot.surf_layer, RA=lot.RA, in_date=datetime.datetime.now(), target_date=lot.target_date, com_id=lot.com_id, prod_type=lot.prod_type, cur_work=issue_code, cur_zone='생산관리')
    db.session.add(lot1)
    db.session.commit()
    return jsonify(result='Lot이 재발행되었습니다.')


@app.route('/lot_split', methods=['POST'])
def lot_split():
    json_encoded=request.data.decode("utf-8")
    json_data=json.loads(json_encoded)
    lot_id=json_data['lot_id']
    lot_sp_code1=json_data['lot_sp_code1'].upper()
    lot_sp_code2=json_data['lot_sp_code2'].upper()
    lot_sn1=json_data['lot_sn1'][:-1]
    lot_sn2=json_data['lot_sn2'][:-1]
    list_lotsn1=lot_sn1.split(',')
    list_lotsn2=lot_sn2.split(',')
    cnt_lot_sn1=len(list_lotsn1)
    cnt_lot_sn2=len(list_lotsn2)
    if len(lot_sn1)==cnt_lot_sn1:
        cnt_lot_sn1=1
    if len(lot_sn2)==cnt_lot_sn2:
        cnt_lot_sn2=1
        
    #cnt_lot_sn1=len([a.split(',') for a in lot_sn1])
    #cnt_lot_sn2=len([b.split(',') for b in lot_sn2])
    if lot_id[-3:-1]=='SP':
        lot_re_count=int(lot_id[-1:])
        lot_re_count+=2
        new_lot_id1=lot_id[:-1] + str(lot_re_count)
        new_lot_id2=lot_id[:-1] + str(lot_re_count+1)
    else:
        new_lot_id1=lot_id + '-' + lot_sp_code1
        new_lot_id2=lot_id + '-' + lot_sp_code2
    lot=Lot.query.filter(Lot.lot_id==lot_id).first()
    issue_code1=lot_sp_code1+'분할'
    issue_code2=lot_sp_code2+'분할'

    lot1=Lot(lot_id=new_lot_id1, company=lot.company, prod_name=lot.prod_name, counts=cnt_lot_sn1, person=lot.person, gen=lot.gen, anod_type=lot.anod_type, prod_serial=lot_sn1, pol_YN=lot.pol_YN, mask_YN=lot.mask_YN, shil_YN=lot.shil_YN, shil_type=lot.shil_type,surf_layer=lot.surf_layer, RA=lot.RA, in_date=datetime.datetime.now(), target_date=lot.target_date, com_id=lot.com_id, prod_type=lot.prod_type, cur_work=issue_code1, cur_zone='생산관리')
    lot2=Lot(lot_id=new_lot_id2, company=lot.company, prod_name=lot.prod_name, counts=cnt_lot_sn2, person=lot.person, gen=lot.gen, anod_type=lot.anod_type, prod_serial=lot_sn2, pol_YN=lot.pol_YN, mask_YN=lot.mask_YN, shil_YN=lot.shil_YN, shil_type=lot.shil_type,surf_layer=lot.surf_layer, RA=lot.RA, in_date=datetime.datetime.now(), target_date=lot.target_date, com_id=lot.com_id, prod_type=lot.prod_type, cur_work=issue_code2, cur_zone='생산관리')
    db.session.add(lot1)
    db.session.add(lot2)
    db.session.commit()
    return jsonify(result='Lot이 분할되었습니다.')



@app.route('/proc_update', methods=['POST', 'GET'])
def proc_update():
    lot_id=request.form['lot_id']
    if request.form['selectto']:
        proclist=request.form.getlist('selectto')
    elif request.form.getlist('auto_procs'):
        proclist=request.form.getlist('auto_procs')
    else:
        flash('공정이 변경되지 않았습니다.')
        return redirect(url_for('lot_info', lot_id=lot_id))
    print(proclist)
    n=len(proclist)
    sqlstring='update lot set '
    for i in range(1,46):
        sqlstring += ' proc' + str(i) + "= NULL ,"
    sqlstring = sqlstring[:-1] + " where lot_id ='" + lot_id + "'"
    result=db.engine.execute(sqlstring)
    if proclist==[]:
        flash('공정이 변경되지 않았습니다.')
        return redirect(url_for('lot_info', lot_id=lot_id))
    else:
        sqlstring2='update lot set '
        for j in range(1,n+1):
            sqlstring2 += ' proc' + str(j) + "= '" + proclist[j-1] + "' ,"
        sqlstring2 = sqlstring2[:-1] + " where lot_id ='" + lot_id + "'"
        result=db.engine.execute(sqlstring2)
        flash('lot정보가 수정되었습니다.')
        return redirect(url_for('lot_info',lot_id=lot_id))