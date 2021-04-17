from flask import Flask, request, Response, render_template, flash, redirect, url_for
from database.db import initialize_db
from database.models import NAT,DB_user
#from flask_mongoengine import MongoEngine
#from mongoengine import *
import subprocess
from flask_login import LoginManager, login_required, login_user, UserMixin
from UserLogin import UserLogin
#from flask.ext.login import UserMixin

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
	'db':'db_name',
	'host':'localhost',
	'port':'27017'
}

app.config['MONGODB_SETTINGS'] = {
	'host':'mongodb://localhost/db_name'
}

#connect('mongoengine_test', host='localhost', port=27017)
db = initialize_db(app)
#db = MongoEngine(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return UserLogin().fromDB(user_id, DB_user)

@app.route("/")
def index():
	return render_template('login.html')

@app.route("/login", methods=["POST","GET"])
def login():
	if request.method == "POST":
		user = DB_user.objects(email=request.form["email"])
		user = user.to_json()
		if user != "[]":
			print(user)
#		print(user.split(":")[4].split(", ")[0].replace('"','').replace(' ',''))
#		print(user.split(":")[2].split(", ")[0].replace('"','').replace(' ',''))
#		print(request.form["email"])
			if (user.split(":")[4].split(", ")[0].replace('"','').replace(' ','')) == request.form['psw']:
				userlogin = UserLogin().create(request.form["email"])
				login_user(userlogin)
				return redirect(url_for('monitoring')) 
		else:
			 return render_template("login.html")
	return render_template("login.html")

@app.route("/registr", methods=["POST","GET"])
def registr():
#	for lunch in DB_user.objects():
#		lunch.delete()
	if request.method == "POST":
		if len(request.form['name']) > 4 and len(request.form["email"]) > 4 and len(request.form['psw']) > 4 and request.form["psw"] == request.form['psw2'] and DB_user.objects(email=request.form["email"]).count() == 0:
			res = DB_user(
				name=request.form['name'],
				email=request.form['email'],
				pasw=request.form['psw']
)
			res.save()
			D_user = []
			for post in DB_user.objects():
				D_user.append(post.to_json())
#			print(D_user)
#			print(DB_user.objects(email=request.form["email"]))
			if res :
				flash("You successfully registered!", "success")
				return redirect(url_for('login'))
			else:
				flash("Error by add in DB!", "error")
		else:
			flash("Error entered fields!", "error")
	return render_template("registr.html")

@app.route('/monitoring')
@login_required
def monitoring():
	cmd = "conntrack -L"
	global post_1
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	out, err = proc.communicate()
	output_proc = out.split("\n")
	output_proc.remove("")
	number_id = 0
	for string_list in output_proc:
		while "  " in string_list:
			string_list = string_list.replace("  ", " ")
		tmp_list = string_list.split(" ")
		if "src=" in tmp_list[3]:
			tmp_list.insert(3, "unknow")
		if str(tmp_list[4])[:4] == str(tmp_list[8])[:4]:
			if str(tmp_list[4])[4:] == str(tmp_list[9])[4:]:
				continue
		if str(tmp_list[4])[4:] == str(tmp_list[8])[4:]:
				continue
		elif str(tmp_list[8]) == "[UNREPLIED]" or tmp_list[4] == "[UNREPLIED]":
			continue
		elif str(tmp_list[0]) == "icmp" and str(tmp_list[5])[4:] == str(tmp_list[9])[4:]:
			continue
		else:
			string_list = tmp_list
			post_1 = NAT(
				track_id=number_id,
				protocol=string_list[0],
				time=string_list[1] + "." + string_list[2],
				src_before=string_list[3],
				dst_before=string_list[4],
				sport_before=string_list[5],
				dport_before=string_list[6],
				src_after=string_list[7],
				dst_after=string_list[8],
				sport_after=string_list[9],
				dport_after=string_list[10],
				code_link=string_list[11],
)
			post_1.save()
			number_id += 1
	posts = []
	for post in NAT.objects():
		posts.append(post.to_json())
#	print(NAT.objects.first())
	for lunch in NAT.objects():
		lunch.delete()
	return render_template('monitoring.html', data=posts)

if __name__ == "__main__":
	app.secret_key = 'super secret key'
	app.run(host='192.168.0.15', debug=False)
