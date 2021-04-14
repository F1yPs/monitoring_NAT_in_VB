from flask import Flask, request, Response, render_template
from database.db import initialize_db
from database.models import NAT
#from flask_mongoengine import MongoEngine
#from mongoengine import *
import subprocess

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

@app.route('/')
def index():
	cmd = "conntrack -L"
	global post_1
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	out, err = proc.communicate()
	output_proc = out.split("\n")
	output_proc.remove("")
	number_id = 0
	for string_list in output_proc:
		string_list = string_list.split()
		if "dprot" in string_list or "sport" in string_list:
			print(string_list)
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
	lunch = NAT.objects.first()
	lunch.delete()
	return render_template('index.html', data=posts)

if __name__ == "__main__":
	app.run(host='192.168.0.15', debug=False)
