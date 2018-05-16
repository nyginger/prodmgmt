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


@app.route('/search/', defaults={'page': 1}, methods=['GET','POST'])
@app.route('/search/<int:page>', methods=['GET','POST'])
def search(page):
    query=request.args.get('query')
    query2=query.replace(" ","_")
    if request.args.get('idx')=='works':
        
        work=[Works.work_name.contains(query)]
        work.append(Works.work_name.contains(query[:-1]))
        work.append(Works.prod_name.contains(query))
        work.append(Works.prod_name.contains(query2))
        work.append(Works.prod_serial.contains(query))
        work.append(Works.prod_serial.contains(query2))
        work.append(Works.company.contains(query))
        work.append(Works.lot_id.contains(query))
        work.append(Works.pub_time.contains(query))
        work.append(Works.person.contains(query))
        qry_works = Works.query.filter(or_(*work)).order_by(Works.pub_time.desc()).paginate(page,30)
        return render_template('msg.html', works=qry_works, query=query, idx='works' )
    elif request.args.get('idx')=='lots':
        lot=[Lot.company.contains(query)]
        lot.append(Lot.lot_id.contains(query))
        lot.append(Lot.prod_name.contains(query2))
        lot.append(Lot.prod_name.contains(query))
        lot.append(Lot.prod_serial.contains(query2))
        lot.append(Lot.prod_serial.contains(query))
        lot.append(Lot.in_date.contains(query))
        lot.append(Lot.target_date.contains(query))
        lot.append(Lot.person.contains(query))
        qry_lots = Lot.query.filter(or_(*lot)).order_by(Lot.in_date.desc()).paginate(page,30)
  
        return render_template('lot.html', lots=qry_lots, query=query, idx='lots' ) 
    else:
        work=[Works.work_name.contains(query)]
        work.append(Works.prod_name.contains(query))
        work.append(Works.prod_name.contains(query2))
        work.append(Works.prod_serial.contains(query))
        work.append(Works.prod_serial.contains(query2))
        work.append(Works.company.contains(query))
        work.append(Works.lot_id.contains(query))
        work.append(Works.pub_time.contains(query))
        work.append(Works.person.contains(query))
        qry_works = Works.query.filter(or_(*work)).order_by(Works.pub_time.desc()).limit(10)
        lot=[Lot.company.contains(query)]
        lot.append(Lot.lot_id.contains(query))
        lot.append(Lot.prod_name.contains(query2))
        lot.append(Lot.prod_name.contains(query))
        lot.append(Lot.prod_serial.contains(query2))
        lot.append(Lot.prod_serial.contains(query))
        lot.append(Lot.in_date.contains(query))
        lot.append(Lot.target_date.contains(query))
        lot.append(Lot.person.contains(query))
        qry_lots = Lot.query.filter(or_(*lot)).order_by(Lot.in_date.desc()).limit(10)
        

        return render_template('searchresult.html', works=qry_works, lots=qry_lots, query=query, idx='' )

