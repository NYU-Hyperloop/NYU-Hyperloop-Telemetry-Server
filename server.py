from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def serve_data():
    return render_template('data.html', data='data')
