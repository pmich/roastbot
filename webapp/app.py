#!/usr/bin/env python
from __future__ import print_function # In python 2.7
from flask import Flask, render_template, flash, request, jsonify
import datetime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os, sys, time, datetime
from gpiozero import LED
from signal import pause
led = LED(2)
led.on()

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
	name = TextField('Name:', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
	form = ReusableForm(request.form)
	templatestate = {
		'starttime' : "",
		'endtime' : "",
		'duration': ""
	}
	name=""
	# print form.errors
	if request.method == 'POST':
		name=request.form.get('name')
		# templatestate['duration'] =request.form.get('name')
		# result = int(templatestate['duration']) * 60
		print(name)
		# str(datetime.timedelta(seconds=seconds))
		# result = time.strftime("%Y-%m-%d_%H:%M:%S")
		# result = str(datetime.timedelta(seconds=seconds))
		# templatestate['endtime'] = templatestate['starttime'] + templatestate['duration']
 		# temp= request.json['key']
 		# jsonify({'key':result})
 		# return render_template('index.html', form=form, name=name)
 	# 	print("starttime " + templatestate['starttime'])
 	# 	print("endttime " + templatestate['endtime'])
 	# 	print("duration " + templatestate['duration'])
		if form.validate():
			# Save the comment here.
			flash(name)
		else:
			flash('Error: All the form fields are required. ')
 
	return render_template('index.html', form=form)

@app.route('/manual', methods=['GET','POST'])
def manual():
	form = ReusableForm(request.form)
	test=""
	message=""
	if request.method == 'POST':
		if request.form['submit'] == 'Heat On':
			message = "This does nothing yet."
			return render_template('manual.html', form=form, message=message)

		elif request.form['submit'] == 'Heat Off':
			message = "Also does nothing."
			return render_template('manual.html', form=form, message=message)

		elif request.form['submit'] == 'Motor On':
			message = "You Turned the Motor On!!"
			led.off()
			return render_template('manual.html', form=form, message=message)

		elif request.form['submit'] == 'Motor Off':
			message = "You Turned the Motor Off!"
			led.on()
			return render_template('manual.html', form=form, message=message)

	else:
		return render_template('manual.html', form=form)

if __name__ == '__main__':
  app.run(debug=True, host='192.168.0.91')
