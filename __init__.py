# -*- coding: utf-8 -*-

'''
import eventlet
import eventlet.wsgi

eventlet.monkey_patch()'''

from eins_app import app,db
import views


if __name__ == '__main__':
#	eventlet.wsgi.server(eventlet.listen(('',8080)), app)
	#socketio.run( app, debug = True )
	app.run(debug=True, host="0.0.0.0", port=6060)

