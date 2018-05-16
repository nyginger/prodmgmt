# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
from sqlalchemy import and_,or_, alias, not_
import json
import os
import datetime
from dateutil.parser import parse
from eins_app import app,db
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen



@app.route('/proclist_info')
def proclist_info():
    stages=Stage.query.all()
    stage_procs=Stage_procs.query.all()
    com_list=Company.query.all()
    return render_template('proclist_info.html',stage_procs=stage_procs,
                                com_list=com_list, new_procs=stages)


@app.route('/update_proclist', methods=['GET', 'POST'])
def update_proclist():
    proc_id=request.form['prod_id']
    proclist=request.form.getlist('auto_procs')

    sqlstring='update stage_procs set '
    sqlstring2='update stage_procs set '
    for i in range(1,26):
        sqlstring += ' proc' + '%02d' % i + "= NULL ,"
    sqlstring=sqlstring[:-2] + " where id= " + proc_id 

    db.engine.execute(sqlstring)
    for j in range(1,len(proclist)+1):
        sqlstring2+=' proc' + '%02d' % j + "= '" + proclist[j-1] + "', "
    sqlstring2=sqlstring2[:-2] + " where id=" + proc_id

    db.engine.execute(sqlstring2)
    stages=Stage.query.all()
    stage_procs=Stage_procs.query.all()
    com_list=Company.query.all()
    return '<script>alert("공정정보가 수정되었습니다.")</script>'


@app.route('/add_procs')
def add_procs():
    com=request.args.get('com')
    prod_cat=request.args.get('prod_cat')
    proclist=request.args.getlist('new_stage_list')
    sqlstring='insert into stage_procs (company,product,'
    for i in range(1,len(proclist)+1):
        sqlstring += ' proc' + '%02d' % i + ","
    sqlstring = sqlstring[:-1] + ") values ('" + com + "','" + prod_cat + "','"
    for j in range(1,len(proclist)+1):
        sqlstring+=proclist[j-1] + "','"
    sqlstring=sqlstring[:-2] + ')'
    print(sqlstring)
    result=db.engine.execute(sqlstring)
    flash('공정정보가 추가되었습니다.')
    stages=Stage.query.all()
    stage_procs=Stage_procs.query.all()
    com_list=Company.query.all()
    return '<script>alert("공정정보가 등록되었습니다.")</script>'





@app.route('/proc_reset')
def proc_reset():
    lot_id=request.args.get('lot_id')
    stages=Stage.query.order_by(Stage.id.asc()).all()
    n=len(stages)
    sqlstring='update lot set '
    for i in range(1,46):
        sqlstring += ' proc' + str(i) + "= NULL,"
    sqlstring = sqlstring[:-1] + " where lot_id ='" + lot_id + "'"
    result=db.engine.execute(sqlstring)
    sqlstring2='update lot set '
    for j in range(1,n+1):
        sqlstring2 += ' proc' + str(j) + "= '" + str(stages[j-1]) + "' ,"
    sqlstring2 = sqlstring2[:-1] + " where lot_id ='" + lot_id + "'"
    result=db.engine.execute(sqlstring2)
    flash('lot정보가 Reset되었습니다.')
    return redirect(url_for('lot_info',lot_id=lot_id))


