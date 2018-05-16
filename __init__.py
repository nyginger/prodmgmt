# -*- coding: utf-8 -*-


from prod_app import app,db
import views


if __name__ == '__main__':

	app.run(debug=True, host="0.0.0.0", port=6060)

