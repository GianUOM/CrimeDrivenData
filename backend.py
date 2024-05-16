# Backend (Flask) - app.py

from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/most_common_crimes')
def most_common_crimes():
    connection = sqlite3.connect('Crime.db')
    cursor = connection.cursor()
    cursor.execute("SELECT title, COUNT(*) AS count FROM crimes GROUP BY title ORDER BY count DESC LIMIT 10")
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
