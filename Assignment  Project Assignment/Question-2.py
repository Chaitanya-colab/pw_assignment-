# Create a Flask app that consumes data from external APIs and displays it to users.
# Try to find an public API which will give you a data and based on that call it and deploy it on cloud platform

from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/pokemon')
def get_pokemon():
    response = requests.get('https://pokeapi.co/api/v2/pokemon/pikachu')
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
