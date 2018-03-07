#!/usr/bin/env python
from __future__ import print_function # In python 2.7
from flask import Flask, render_template, flash, request, jsonify
from flask_socketio import SocketIO, emit
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
socketio = SocketIO(app)

class ReusableForm(Form):
	name = TextField('Name:', validators=[validators.required()])
 
@app.route("/", methods=['GET', 'POST'])
def hello():
	form = ReusableForm(request.form)
	name=""
	# print form.errors
	if request.method == 'POST':
		name=request.form.get('name')
		print(name)
		if form.validate():
			# Save the comment here.
			return render_template('index.html', form=form, name=name)
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
		elif request.form['submit'] == 'Heat Off':
			message = "Also does nothing."
		elif request.form['submit'] == 'Motor On':
			message = "You Turned the Motor On!!"
			led.off()
		elif request.form['submit'] == 'Motor Off':
			message = "You Turned the Motor Off!"
			led.on()
		return render_template('manual.html', form=form, message=message)
	else:
		return render_template('manual.html', form=form)

@socketio.on('my event')
def handle_my_custom_event(json):
	# socketio.send("start")
	led.off()
	finaltime = json['starttime'] + json['roasttime']
	print('received something: ' + str(json))
	# socketio.emit('my response', json)
	print("start time from client is: " + str(json['starttime']))
	print("final time is: " + str(finaltime))
	json.update({'finaltime':finaltime})
	for i in range(long(json['starttime']),finaltime+1000,1000):
	 	print("timer count is: " + str(i))
	 	socketio.sleep(1)
	 	json.update({'timeleft':finaltime-i})
	 	socketio.emit('my response', json)
	# socketio.emit('my response', "Finished!")
	json.update({'msg':"Finished!"})
	socketio.emit('my response', json)
	led.on()

if __name__ == '__main__':
  socketio.run(app, debug=True, host="192.168.0.91" )
