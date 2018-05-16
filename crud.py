from eins_app import app,db,APP_ROOT
from models.update_data import ins_workdata, ins_lotdata, update_prodtype,update_lot_prod


if __name__ == '__main__':
	#ins_workdata('작업진행2.csv')
	#ins_lotdata('lot3.csv')	
	df=update_prodtype()
	#print(df[1]['count'])
	for row in df:
		prod_cat=row['prod']
		for lot_id in row['lot_id']:
			update_lot_prod(lot_id,prod_cat)
	
	print('Completed!')