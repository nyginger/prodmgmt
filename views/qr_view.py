# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
import json
import os
import pyqrcode
from eins_app import app,db,APP_ROOT
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen



@app.route('/qr')
def qr():
    return render_template('qr.html')


@app.route('/qrcode', methods=['GET'])
def qrcode():
    q=request.args.get('q')
    #byte_q=bytes(q,'utf-8')
    #dec_q=byte_q.decode('utf-8')
    target=os.path.join(APP_ROOT, 'qrcode')
    if not os.path.isdir(target):
        os.mkdir(target)
    qr=pyqrcode.create(q)
    qrfile=target + os.sep + q + '.png'
    qr.png(qrfile, scale=7)
    return send_file(qrfile)


import requests

@app.route('/readqr', methods=['GET', 'POST'])
def readqr():
    url="http://api.qrserver.com/v1/read-qr-code/"
    result=[]
    
    for file in request.files.getlist("file"):
    
        qrfile=[('file',file)]
        r=requests.post(url=url, files=qrfile)
        json_load=json.loads(r.text)
        json_data=json_load[0]['symbol']
        response=json_data[0]['data']
        result.append(response)    

    return render_template('qr.html' ,qrtext=result)
