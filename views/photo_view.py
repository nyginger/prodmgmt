# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for
import json
import os
import datetime
from dateutil.parser import parse
from eins_app import app,db,APP_ROOT
from models import Works,Persons,Stage,Lot,Stage_procs, \
                    Anod,Company,Product,Gen



@app.route('/upload')
def upload():
    return render_template("upload.html")


from PIL import Image, ImageFont, ImageDraw

@app.route('/up_result', methods=['GET', 'POST'])
def up_result():
    lot_id=request.form['lot_id']
    company=request.form['company']
    prod_name=request.form['prod_name'].replace(" ","_")
    in_out=request.form['in_out']
    message=request.form['message']
    stage=request.form['work_name']
    person=request.form['person']

    #stage=Stage.query.filter_by(work=work_name).first()
    work_name=Stage.query.filter_by(id=stage).first()
    print(stage)

    if not lot_id or lot_id=='':
        return redirect(url_for('index'))
    else:
        target=os.path.join(APP_ROOT, 'image')
        if not os.path.isdir(target):
            os.mkdir(target)
        target2=os.path.join(target, lot_id )
        if not os.path.isdir(target2):
            os.mkdir(target2)
        thumb_dir=os.path.join(APP_ROOT, 'thumbnail', lot_id)
        thumb_size=128,128
        if not os.path.isdir(thumb_dir):
            os.mkdir(thumb_dir)
        i=0
        for file in request.files.getlist("file"):
            r='%03d' % i
            timeserial=datetime.datetime.now()
            pub_time=timeserial.strftime('%Y-%m-%d @ %H:%M:%S')
            filename, file_ext = os.path.splitext(file.filename)
            newfilename= lot_id + '_' + stage + '_' + r + '_' + timeserial.strftime('(%Y%m%d_%H%M%S)') + file_ext
            print(newfilename)
            destination='/'.join([target2,newfilename])
            file.save(destination)
            img = Image.open(file)
            img.thumbnail(thumb_size)
            thumb_dest='/'.join([thumb_dir,'thumbnail_' + newfilename])
            img.save(thumb_dest)
            work=Works(work_name=work_name.work, lot_id=lot_id,company=company, prod_name=prod_name, person=person, message=message, stage=stage, pub_time=timeserial, filename=file.filename, filelocation=newfilename)
            db.session.add(work)
            db.session.commit()
            i=i+1
         #return redirect(url_for('index'))
        return redirect(url_for('get_gallery', lot_id=lot_id))


@app.route('/gallery')
def get_gallery():
    lot_id=request.args.get('lot_id')
    try:
        image_names=os.listdir(os.path.join(APP_ROOT, 'thumbnail', lot_id  ))
        img_stg={}
        for n in range(1,10):
            img_stg['%d' % n]=[]

        for img in image_names:
            filename,file_ext =os.path.splitext(img)
            if file_ext=='.jpg' or file_ext=='.png' or file_ext=='.gif':
                fileinfo=img.split('_')
                n='%s' % fileinfo[2][:1]
                img_stg[n].append(img)

        stages=Stage.query.all()
        return render_template("gallery.html", lot_id=lot_id, stages=stages,
                                img_stg1=img_stg['1'], img_stg2=img_stg['2'],
                                img_stg3=img_stg['3'], img_stg4=img_stg['4'],
                                img_stg5=img_stg['5'], img_stg9=img_stg['9'],
                                img_stg6=img_stg['6'], img_stg7=img_stg['7']
                                )
    except:
        return render_template("gallery.html", lot_id=lot_id, image_names='')


import base64

@app.route('/photoupload', methods=['GET', 'POST'])
def photoupload():
    target=os.path.join(APP_ROOT, 'image')
    if not os.path.isdir(target):
        os.mkdir(target)
    img_data=request.form['base64Image']
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(img_data))
    #return redirect(url_for('index'))
    return redirect(url_for('get_gallery', lot_id=lot_id))


@app.route('/return_file')
def return_file():
    lot_id=request.args.get('lot_id')
    filename=bytes(request.args.get('filename'),'utf-8')
    filename=filename.decode('utf-8')
    filelocation=request.args.get('filelocation')
    imgfile="image" + os.sep + lot_id + os.sep + filelocation

    return send_file(imgfile)


@app.route('/show_file')
def show_file():
    lot_id=request.args.get('lot_id')
    thumb_file=request.args.get('filelocation')
    filelocation=thumb_file[10:]
    imgfile="image"+ os.sep + lot_id + os.sep + filelocation

    return send_file(imgfile)



@app.route('/up_result/<filename>', methods=['GET', 'POST'])
def send_image(filename):
    try:
        lot_id=request.args.get('lot_id')
        imgdir="thumbnail" + os.sep + lot_id + os.sep
        return send_from_directory(imgdir, filename)
    except:
        return None





@app.route('/create_img', methods=['GET'])
def create_img():
    if request.args.get('username'):
        username=request.args.get('username')
    if request.args.get('work_name'):
        work_name=request.args.get('work_name')
    target=os.path.join(APP_ROOT, 'thumbnail')
    if not os.path.isdir(target):
        os.mkdir(target)
    origin=os.sep.join([APP_ROOT,'static', os.sep, 'image.jpg'])
    img = Image.open(origin)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 16)
    draw.text((120, 120), work_name , font=font, fill='#FFF')
    destination=os.sep.join([target,'sample.jpg'])
    img.save(destination)
    return render_template('index2.html')

