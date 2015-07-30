from vagupu import app
from flask import render_template, request, redirect, render_template, session, url_for
from config import log
from xml.dom import minidom
from models import *
import base64

def getrecords():
	'''
	For parsing username and password from data.xml
	'''
	fin = open(r"/home/dell/vagupu/vagupu/data.xml")
	xmldoc =  minidom.parse(fin)
	userdict = {}
	userlist = xmldoc.getElementsByTagName("user")
	for elem in userlist:
		userdict[elem.getAttribute("username")] = elem.getAttribute("password")
	return userdict



@app.route('/')
@app.route('/login_1/', methods = ['GET','POST'])
def login_1():
	'''
	Matches username and password with the credentials stored in data.xml
	'''
	error = None
	if request.method == 'POST':
		data = getrecords()
		if request.form['username'] not in data.keys():
			error = 'Invalid username'
			log.error(request.form['username'])
			log.error(error)
		elif data[request.form['username']] != request.form['password'] :
			error = 'Invalid password'
			log.error(request.form['password'])
			log.error(error)
		else:
			session['logged_in'] = True
			log.info("Successful Login")

			return redirect(url_for('welcome', username = request.form['username']))	

	return render_template('login.html', error=error)

@app.route('/login/', methods = ['GET','POST'])
def login():
	'''
	Matches the username and password provided by user with the 
	username and encrypted password in stored in database
	'''
	error = None   
	if request.method == 'POST':
		user = User.query.filter_by(username=request.form['username']).first()
		if not user:
			error = 'Invalid username'
			log.error(request.form['username'])
			log.error(error)
			
		elif (base64.decodestring(user.password)!= request.form['password']):
			error = 'Invalid password'
			log.error(request.form['password'])
			log.error(error)
		else:
			session['logged_in'] = True
			log.info("Successful Login")

			return redirect(url_for('welcome', username = request.form['username']))		
					
	return render_template('login.html', error=error)



@app.route('/welcome/<username>')
def welcome(username):

	'''
	User is redirected to Welcome screen on successful login
	'''
	log.info("User %s redirected to Welcome screen" %(username,))
	return render_template('user.html', username = username)


@app.route('/signup/', methods=['GET','POST'])
def signup():
	'''
	New user can sign up at Sign Up screen and the username and encoded password is stored in the 
	database. User is redirected to Login screen
	'''
	if request.method == 'POST':
		password = base64.encodestring(request.form['password'])	
		user = User(request.form['username'], password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))	
	return render_template('signup.html')