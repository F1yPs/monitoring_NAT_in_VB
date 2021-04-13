from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
	cmd = "conntrack -L"
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	out, err = proc.communicate()
	output_proc = out.split("\n")
	output_proc.remove("")
	for string_list in output_proc:
		return str(string_list.split())

if __name__ == "__main__":
	app.run(host='192.168.0.15')
