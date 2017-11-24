from flask import Flask, render_template, request

app = Flask(__name__)

#PART 1
@app.route('/person/<name>/<int:age>')
def person(name, age):
	return render_template('person.html', name=name, age=age)

    
# PART2
@app.route('/calculate')
def calculate():
	pass

if __name__ == '__main__':
	app.run(debug=True)