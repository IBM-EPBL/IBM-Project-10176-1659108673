from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def Final():
    return render_template('Final.html')

app.run(debug=True)