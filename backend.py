from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

database_path = "Crime.db"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/most_common_crimes')
def most_common_crimes():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT title, COUNT(*) AS count FROM crimes GROUP BY title ORDER BY count DESC LIMIT 10")
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/api/most_common_locations')
def most_common_locations():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name, COUNT(*) AS count FROM locations GROUP BY name ORDER BY count DESC LIMIT 10")
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/api/crimes_by_location', methods=['GET'])
def crimes_by_location():
    location = request.args.get('location')
    connection = sqlite3.connect(database_path)
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
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT l.name, COUNT(*) AS count
        FROM locations l
        JOIN crimes c ON l.article_id = c.article_id
        WHERE c.title = ?
        GROUP BY l.name
        ORDER BY count DESC
        LIMIT 10
    """, (crime,))
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/api/crimes_in_location', methods=['GET'])
def crimes_in_location():
    location = request.args.get('location')
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT c.title, COUNT(*) AS count
        FROM crimes c
        JOIN locations l ON c.article_id = l.article_id
        WHERE l.name = ?
        GROUP BY c.title
        ORDER BY count DESC
        LIMIT 10
    """, (location,))
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/crime/<crime>')
def crime_locations(crime):
    return render_template('commonPlacesForCrime.html', crime=crime)

@app.route('/location/<location>')
def location_crimes(location):
    return render_template('commonCrimesForPlace.html', location=location)

if __name__ == '__main__':
    app.run(debug=True)
