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


@app.route( '/work/<int:zone_id>' ,  defaults={'page': 1},methods=['GET','POST'])
@app.route('/work/<int:zone_id>/<int:page>',methods=['GET','POST'])
#@login_required
def work(zone_id,page):
    stages=Stage.query.all()
    if zone_id==0:
        lots=Lot.query.filter(Lot.cur_work!="출고처리",Lot.company!='',Lot.proc1!='').order_by(Lot.company.asc()).paginate(page,50)
        zone={'zone':'전체', 'zone_id':0}
    else:
        zone=Stage.query.filter(Stage.zone_id==zone_id).first()
        lots=Lot.query.filter(Lot.cur_zone==zone.zone,Lot.company!='',Lot.proc1!='').order_by(Lot.company.asc()).paginate(page,50)
    print(zone)
    return render_template('work_lot.html', zone=zone, lots=lots)


        