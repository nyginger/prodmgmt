# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
from sqlalchemy import and_,or_, alias, not_
import json
import os
import datetime
from dateutil.parser import parse
from prod_app import app,db
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen




@app.route('/msg/', defaults={'page': 1}, methods=['GET','POST'])
@app.route('/msg/<int:page>', methods=['GET','POST'])
def msg(page):
    works=Works.query.order_by(Works.pub_time.desc()).paginate(page,20)
    if not works and page != 1:
        abort(404)
    return render_template( 'msg.html', works=works, idx='works', query='')



@app.route('/delete', methods=['POST'])
def delete():
    json_encoded=request.data.decode("utf-8")
    json_data=json.loads(json_encoded)
    db_table=json_data['datatable']
    data_id=int(json_data['data_id'])
    if db_table=='works':
        rec=Works.query.filter(Works.id==data_id).first()
    elif db_table=='lot':
        rec=Lot.query.filter(Lot.id==data_id).first()
    current_db_sessions = db.session.object_session(rec)
    current_db_sessions.delete(rec)
    current_db_sessions.commit()
    return render_template('index.html')


