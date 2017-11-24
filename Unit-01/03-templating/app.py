from flask import Flask, render_template, request

app = Flask(__name__)

#PART 1
@app.route('/person')
def person():
  return 'Your name {name} and your age {age}'
    


#PART2
# @app.route('/calculate')
# def calculate():
# 	pass

if __name__ == '__main__':
	app.run(debug=True)