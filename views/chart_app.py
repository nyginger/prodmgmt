from __future__ import with_statement
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, jsonify
import sqlite3
import pandas as pd
import numpy as np
import os
import eventlet.wsgi

app= Flask(__name__)
DATABASE=os.path.abspath(os.getcwd()) + "\\DATABASE.db"
conn = sqlite3.connect(DATABASE, check_same_thread=False)
c=conn.cursor()
query_lot="select * from lot "
data_lot=pd.read_sql_query(query_lot, conn)
data_lot['Yr']=pd.DatetimeIndex(data_lot['in_date']).strftime("%Y")
data_lot['Mon']=pd.DatetimeIndex(data_lot['in_date']).strftime("%m")
data_lot['Date']=pd.DatetimeIndex(data_lot['in_date']).strftime("%Y-%m-%d")
data_lot['Date']=data_lot['Date'].apply(pd.to_datetime)
data_lot['ComPro']=data_lot['company'] + '_' + data_lot['prod_name']
data_lot['Yr']=data_lot['Yr'].apply(pd.to_numeric)
data_lot['Mon']=data_lot['Mon'].apply(pd.to_numeric)
data_lot['counts']=data_lot['counts'].apply(pd.to_numeric)
data_lot['ProdType']=data_lot['prod_name']
data_lot.loc[(data_lot['prod_name'].str.contains('A1')==True) & (data_lot['prod_name'].str.contains('상부전극')==True), 'ProdType']='3'
data_lot.loc[(data_lot['prod_name'].str.contains('A1')==True) & (data_lot['prod_name'].str.contains('하부전극')==True), 'ProdType']='4'
data_lot.loc[(data_lot['prod_name'].str.contains('RWD')==True), 'ProdType']='13'
data_lot.loc[(data_lot['prod_name'].str.contains('SCE')==True), 'ProdType']='14'
data_lot.loc[(data_lot['prod_name'].str.contains('SHOWER_HEAD')==True), 'ProdType']='15'
data_lot.loc[(data_lot['prod_name'].str.contains('TRAY_PLATE')==True), 'ProdType']='16'
data_lot.loc[((data_lot['prod_name'].str.contains('A2')==True) | (data_lot['prod_name'].str.contains('5.5G')==True) | (data_lot['gen'].str.contains('5.5G')==True)) & ((data_lot['prod_name'].str.contains('DIFFUSER')==True) | (data_lot['prod_name'].str.contains('D/F')==True)), 'ProdType']='5'
data_lot.loc[((data_lot['prod_name'].str.contains('A3')==True) | (data_lot['prod_name'].str.contains('6G')==True) | (data_lot['gen'].str.contains('6G')==True)) & ((data_lot['prod_name'].str.contains('DIFFUSER')==True) | (data_lot['prod_name'].str.contains('D/F')==True)), 'ProdType']='9'
data_lot.loc[((data_lot['prod_name'].str.contains('A2')==True) | (data_lot['prod_name'].str.contains('5.5G')==True) | (data_lot['gen'].str.contains('5.5G')==True)) & ((data_lot['prod_name'].str.contains('SHADOW_FRAME')==True) | (data_lot['prod_name'].str.contains('S/F')==True)), 'ProdType']='6'
data_lot.loc[((data_lot['prod_name'].str.contains('A3')==True) | (data_lot['prod_name'].str.contains('6G')==True) | (data_lot['gen'].str.contains('6G')==True)) & ((data_lot['prod_name'].str.contains('SHADOW_FRAME')==True) | (data_lot['prod_name'].str.contains('S/F')==True)), 'ProdType']='10'
data_lot.loc[((data_lot['prod_name'].str.contains('A1')==True) | (data_lot['prod_name'].str.contains('4G')==True) | (data_lot['gen'].str.contains('4G')==True)) & ((data_lot['prod_name'].str.contains('SUSCEPTOR')==True) | (data_lot['prod_name'].str.contains('S/T')==True) | (data_lot['prod_name'].str.contains('SCT')==True)), 'ProdType']='1'
data_lot.loc[((data_lot['prod_name'].str.contains('A2')==True) | (data_lot['prod_name'].str.contains('5.5G')==True) | (data_lot['gen'].str.contains('5.5G')==True)) & ((data_lot['prod_name'].str.contains('SUSCEPTOR')==True) | (data_lot['prod_name'].str.contains('S/T')==True) | (data_lot['prod_name'].str.contains('SCT')==True)), 'ProdType']='7'
data_lot.loc[((data_lot['prod_name'].str.contains('A3')==True) | (data_lot['prod_name'].str.contains('6G')==True) | (data_lot['gen'].str.contains('6G')==True)) & ((data_lot['prod_name'].str.contains('SUSCEPTOR')==True) | (data_lot['prod_name'].str.contains('S/T')==True) | (data_lot['prod_name'].str.contains('SCT')==True)), 'ProdType']='11'
data_lot.loc[((data_lot['prod_name'].str.contains('A1')==True) | (data_lot['prod_name'].str.contains('4G')==True) | (data_lot['gen'].str.contains('4G')==True)) & ((data_lot['prod_name'].str.contains('LINER')==True) | (data_lot['prod_name'].str.contains('이중월')==True) | (data_lot['prod_name'].str.contains('이중WALL')==True)), 'ProdType']='2'
data_lot.loc[((data_lot['prod_name'].str.contains('A2')==True) | (data_lot['prod_name'].str.contains('5.5G')==True) | (data_lot['gen'].str.contains('5.5G')==True)) & ((data_lot['prod_name'].str.contains('LINER')==True) | (data_lot['prod_name'].str.contains('이중월')==True) | (data_lot['prod_name'].str.contains('이중WALL')==True)), 'ProdType']='8'
data_lot.loc[((data_lot['prod_name'].str.contains('A3')==True) | (data_lot['prod_name'].str.contains('6G')==True) | (data_lot['gen'].str.contains('6G')==True)) & ((data_lot['prod_name'].str.contains('LINER')==True) | (data_lot['prod_name'].str.contains('이중월')==True) | (data_lot['prod_name'].str.contains('이중WALL')==True)), 'ProdType']='12'

data_lot['ProdType']=pd.to_numeric(data_lot['ProdType'], errors='coerce')
data_lot.loc[(data_lot['ProdType'].isnull()), 'ProdType']='17'
data_lot['ProdType']=data_lot['ProdType'].astype(int)
data_lot['counts']=pd.to_numeric(data_lot['counts'], errors='coerce')
data_lot.loc[(data_lot['counts'].isnull()), 'counts']=0
data_lot['in_date']=pd.to_datetime(data_lot['in_date'], errors='coerce')
data_lot=data_lot.set_index(['in_date'])


query_work="select * from works "
data_work=pd.read_sql_query(query_work, conn)
data_work=data_work.dropna(subset=['work_no'],how='any',axis=0)
data_work['Yr']=pd.DatetimeIndex(data_work['pub_time']).strftime("%Y")
data_work['Mon']=pd.DatetimeIndex(data_work['pub_time']).strftime("%m")
data_work['Week']=pd.DatetimeIndex(data_work['pub_time']).strftime("%V")
data_work['Day']=pd.DatetimeIndex(data_work['pub_time']).strftime("%d")
data_work['Date']=pd.DatetimeIndex(data_work['pub_time']).strftime("%Y-%m-%d")
data_work['Yr']=data_work['Yr'].apply(pd.to_numeric)
data_work['Mon']=data_work['Mon'].apply(pd.to_numeric)
data_work['Week']=data_work['Week'].apply(pd.to_numeric)
data_work['Day']=data_work['Day'].apply(pd.to_numeric)
data_work['pub_time']=data_work['pub_time'].apply(pd.to_datetime)
data_work['zone']=data_work['stage'].map(lambda x: x[:1])
data_prod = pd.DataFrame({'A' : []})
data_prod['lot_id']=data_lot['lot_id']
data_prod['ProdType']=data_lot['ProdType']
data_work=pd.merge(data_work,data_prod, on='lot_id')
data_work['prod_id']=data_work['ProdType'].astype(int)

query_prod="select prod_id,prod_name from product"
df_prod=pd.read_sql_query(query_prod, conn)
df_prod['prod_cat']=df_prod['prod_name']
data_work=pd.merge(data_work,df_prod, on='prod_id')
data_work['ComPro']=data_work['company'] + '_' + data_work['prod_cat']
data_work['ComProStage']=data_work['ComPro'] + '_' + data_work['stage']
data_work['min_by_lot_stage']=data_work.groupby(['work_no2'])['pub_time'].diff()
data_work['min_by_lot_stage']=data_work['min_by_lot_stage'].dt.total_seconds().div(60, fill_value=0)
data_work=data_work[(data_work['min_by_lot_stage']>0) & (data_work['min_by_lot_stage']<=1500)]
#data_work['counts']=pd.to_numeric(data_work['counts'], errors='coerce')
#data_work.loc[(data_work['counts'].isnull()), 'counts']=0
#data_work['person_count']=data_work['person_count'].apply(pd.to_numeric,errors='coerce')
#data_work=data_work.drop(data_work['person_count'].isnull()==True)


@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/chart_lot', methods=['GET'])
def chart_lot():
    prod_list=c.execute('select prod_id,prod_name from product order by prod_id asc').fetchall()
    com_list=c.execute('select * from company').fetchall()
    if request.args.get('ctype'):
        ctype=request.args.get('ctype')
    else:
        ctype=1
    return render_template('chart_lot.html',  
                         prod=request.args.get('prod'), com=request.args.get('com'),  
                        prod_list=prod_list, com_list=com_list, ctype=ctype)


@app.route('/chart_work', methods=['GET'])
def chart_work():
    zone_list=c.execute('select zone_id,zone from stage group by zone order by zone_id').fetchall()
    prod_list=c.execute('select prod_id,prod_name from product order by prod_id asc').fetchall()
    com_list=c.execute('select * from company').fetchall()
    if request.args.get('ctype'):
        ctype=request.args.get('ctype')
    else:
        ctype=1
    return render_template('chart_work.html',lot_id=request.args.get('lot_id'),
                            prod=request.args.get('prod') ,com=request.args.get('com'), 
                            zone=request.args.get('zone'), zone_list=zone_list,
                            prod_list=prod_list, com_list=com_list, ctype=ctype)
                            

@app.route('/chrtdata_lotcnt', methods=['GET'])
def chrtdata_lotcnt():
    ctype=int(request.args.get('ctype'))
    product=request.args.get('product')
    company=request.args.get('company')
    selected =data_lot
    if (company!= "전체" and company.upper()!='NULL'):
        selected=selected[selected['com_id']== int(company) ]
    prod_table=pd.pivot_table(selected,index=[lambda x: str(x.year) + '-' + str('%02d' % x.month)],values=["counts"],columns=["ProdType"],aggfunc=[np.sum,len],fill_value=0)
    try:
        prod_table=prod_table.drop(('len','counts',0),1)
    except:
        prod_table=prod_table
    try:
        prod_table=prod_table.drop(('sum','counts',0),1)
    except:
        prod_table=prod_table
    try:
        prod_table=prod_table.drop(('len','counts',17),1)
    except:
        prod_table=prod_table
    try:
        prod_table=prod_table.drop(('sum','counts',17),1)
    except:
        prod_table=prod_table
    lot_table=prod_table
    try:
        lot_table[('sum','counts',2)]=prod_table[('len','counts',2)]
    except:
        lot_table=prod_table
    try:
        lot_table[('sum','counts',8)]=prod_table[('len','counts',8)]
    except:
        lot_table=prod_table
    try:
        lot_table[('sum','counts',12)]=prod_table[('len','counts',12)]
    except:
        lot_table=prod_table
    try:
        lot_table=lot_table[('sum','counts')]
    except:
        lot_table=prod_table
    prod=c.execute('select prod_id,prod_name from product').fetchall()
    if ctype==1 :
        if (product!= "전체" and product.upper()!='NULL'):
            selected=lot_table[int(product)]
            labels=selected.index.get_level_values(0).tolist()
            values=selected.tolist()
            return jsonify({'labels': labels,'values' : values})
        else:
            selected=lot_table
            return jsonify({'labels': [],'values' : [] })

    else:
        year=int(request.args.get('year'))
        month=int(request.args.get('month'))
        YrMo= str(year) + '-' + str('%02d' % month)
        try:
            selected=lot_table.loc[YrMo]
        except:
            return jsonify({'labels':[],'values' : [] })
        if (product!= "전체" and product.upper()!='NULL'):
            labels=list()
            temp=[]
            values=[]
            temp.append(YrMo)
            labels.append(temp)
            values.append(selected[int(product)].tolist())
            
            return jsonify({'labels':YrMo,'values' : values})
        else:
            temp_labels=selected.index.get_level_values(0).tolist()
            labels=[]
            for pl in temp_labels:
                for pr in prod:
                    if pl==pr[0]:
                        labels.append(pr[1])
            values=selected.tolist()
            return jsonify({'labels':labels,'values' : values})


import random

@app.route('/chrtdata_work', methods=['GET'])
def chrtdata_work():

    ctype=int(request.args.get('ctype'))
    stage=c.execute("select id,work from stage where zone_id !=9 ").fetchall()
    cnt_st=int(c.execute("select count(id) from stage where zone_id !=9 ").fetchone()[0])
    selected=data_work

    if ctype==1 :
        query_date=request.args.get('date')
        selected=selected[(selected['Date']==query_date)]
        selected=selected.groupby( ['stage'])['min_by_lot_stage'].sum().to_frame() 
        selected=selected.astype(int, errors='ignore')
        selected=selected[selected['min_by_lot_stage']>0]
        labels=selected.index.get_level_values(0).tolist()
        newlabels=[]
        colors=[]
        for i in range(0,len(labels)):
            for j in range(0,cnt_st):
                if int(labels[i])==stage[j][0]:
                    newlabels.append(stage[j][1])
            r = lambda: random.randint(0,255)
            color= "rgba(%s" % r() + ", %s" % r() + ", %s" % r() + ",0.3)"
            colors.append(color)
        values=selected['min_by_lot_stage'].tolist()
        return jsonify({'labels':newlabels,'values' : values, 'colors':colors})

    elif ctype==2 :
        lot_id=request.args.get('lot_id')
        selected=selected[(selected['lot_id']==lot_id)]
        selected=selected.groupby( ['stage'])['min_by_lot_stage'].sum().to_frame() 
        selected=selected.astype(int, errors='ignore')
        selected=selected[selected['min_by_lot_stage']>0]
        labels=selected.index.get_level_values(0).tolist()
        newlabels=[]
        colors=[]
        for i in range(0,len(labels)):
            for j in range(0,cnt_st):
                if int(labels[i])==stage[j][0]:
                    newlabels.append(stage[j][1])
            r = lambda: random.randint(0,255)
            color= "rgba(%s" % r() + ", %s" % r() + ", %s" % r() + ",0.3)"
            colors.append(color)
        values=selected['min_by_lot_stage'].tolist()
        return jsonify({'labels':newlabels,'values' : values, 'colors' : colors})
    
    else:
        if request.args.get('zone'):
            zone=request.args.get('zone')
            if zone !='null':
                selected=selected[selected['zone']==zone]
        if request.args.get('period') :
            query_period=request.args.get('period')
        if request.args.get('company') :
            company=request.args.get('company')
            if (company!= "전체" and company !='null'):
                selected=selected[selected['com_id']==int(company)]
        if request.args.get('product'):
            product=request.args.get('product')
            if (product!= "전체" and product !='null'):
                selected=selected[selected['prod_id']==int(product)]
        selected=selected.groupby( ['ComProStage'])['min_by_lot_stage'].mean().to_frame() 
        selected=selected.astype(int, errors='ignore')
        selected=selected[selected['min_by_lot_stage']>0]
        labels=selected.index.get_level_values(0).tolist()
        newlabels=[]
        for i in range(0,len(labels)):
            for j in range(0,cnt_st):
                if int(labels[i][-3:])==stage[j][0]:
                    newlabels.append(labels[i][:-3] + stage[j][1])
        values=selected['min_by_lot_stage'].tolist()
        df=selected.sort_values('min_by_lot_stage',ascending=False)
        return jsonify({'labels':newlabels,'values' : values})


if __name__=='__main__':
    #app.run(debug=True)
    eventlet.wsgi.server(eventlet.listen(('',5000)), app)