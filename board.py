# -*- coding: utf-8 -*-
'''
OctoDog Web Application
Main Web Function
#TODO-change url name 
http://projboard.sinaapp.com/
@author: bambooom
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import URL
from dbhandler import fetch_repos_table, fetch_name_list, add_repo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'OctoDog key'

#repos_table = 
reponame_list = fetch_name_list(fetch_repos_table())

def update_list():
	global reponame_list
	#repos_table = fetch_repos_table()
	reponame_list = fetch_name_list(fetch_repos_table())
	return reponame_list

def get_repo_name(repo_url):
	'''
	Parse the url of the repository to get the name.
	'''
	from urlparse import urlparse, urlsplit
	foo = urlparse(repo_url)
	return foo.path.split('/')[2]


@app.route('/',methods=['GET'])
def board():
	global reponame_list
	reponame_list = update_list()
	return render_template("index.html", repos = reponame_list)


class InsertPro(Form):
	repo_url = StringField("Add your project", validators=[URL(message='\
		Sorry, this is not a valid URL')])
	submit = SubmitField('Submit')


@app.route('/project', methods=['POST','GET'])
def insert_pro():
	form = InsertPro()
	global reponame_list
	if form.validate_on_submit():
		session['repo_url'] = form.repo_url.data
		url = session.get('repo_url')
		reponame = get_repo_name(url)
		new_repo = reponame, url
		add_repo(new_repo)
		reponame_list = update_list()
		# flash("Added Successfully.")
		return redirect(url_for('show_pro', reponame=reponame, 
			repos=reponame_list, _external=True))	
	return render_template("project.html", repos=reponame_list, 
		form=form, repo_url=session.get('repo_url'))

@app.route('/project/<reponame>', methods=['GET'])
def show_pro(reponame):
	# show the project profile with info
	global reponame_list
	reponame_list = update_list()
	return render_template("profile.html", reponame=reponame, 
		repos=reponame_list)
	#return 'showcase for project %s' % reponame



if __name__ == '__main__':
	app.run(debug=True)