# Backend (Flask) - app.py

from flask import Flask, jsonify, render_template, request
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

@app.route('/api/most_common_locations')
def most_common_locations():
    connection = sqlite3.connect('Crime.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name, COUNT(*) AS count FROM locations GROUP BY name ORDER BY count DESC LIMIT 10")
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/api/crimes_by_location', methods=['GET'])
def crimes_by_location():
    location = request.args.get('location')
    connection = sqlite3.connect('Crime.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT c.title
        FROM crimes c
        JOIN locations l ON c.article_id = l.article_id
        WHERE l.name = ?
    """, (location,))
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/api/locations_by_crime', methods=['GET'])
def locations_by_crime():
    crime = request.args.get('crime')
    connection = sqlite3.connect('Crime.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT l.name
        FROM locations l
        JOIN crimes c ON l.article_id = c.article_id
        WHERE c.title = ?
    """, (crime,))
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
