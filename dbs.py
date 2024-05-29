import sqlite3
import os
import spacy_crime
import csv

def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crimes (
        id INTEGER PRIMARY KEY,
        title TEXT,
        article_id INTEGER,
        FOREIGN KEY (article_id) REFERENCES articles(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dates (
        id INTEGER PRIMARY KEY,
        text TEXT,
        article_id INTEGER,
        FOREIGN KEY (article_id) REFERENCES articles(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        article_id INTEGER,
        FOREIGN KEY (article_id) REFERENCES articles(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT,
        article_id INTEGER,
        FOREIGN KEY (article_id) REFERENCES articles(id)
    )
    """)

def insert_data(cursor, entities, article_id):
    for crime in entities["Crime"]:
        cursor.execute("SELECT id FROM crimes WHERE title = ? AND article_id = ?", (crime, article_id))
        existing_crime = cursor.fetchone()
        if not existing_crime:
            cursor.execute("INSERT INTO crimes (title, article_id) VALUES (?, ?)", (crime, article_id))

    for date in entities["Date"]:
        cursor.execute("SELECT id FROM dates WHERE text = ? AND article_id = ?", (date, article_id))
        existing_date = cursor.fetchone()
        if not existing_date:
            cursor.execute("INSERT INTO dates (text, article_id) VALUES (?, ?)", (date, article_id))

    for location in entities["Location"]:
        cursor.execute("SELECT id FROM locations WHERE name = ? AND article_id = ?", (location, article_id))
        existing_location = cursor.fetchone()
        if not existing_location:
            cursor.execute("INSERT INTO locations (name, article_id) VALUES (?, ?)", (location, article_id))

    for name in entities["Names"]:
        cursor.execute("SELECT id FROM people WHERE name = ? AND article_id = ?", (name, article_id))
        existing_name = cursor.fetchone()
        if not existing_name:
            cursor.execute("INSERT INTO people (name, article_id) VALUES (?, ?)", (name, article_id))

connection = sqlite3.connect(os.path.join('Crime.db'))
cursor = connection.cursor()

create_tables(cursor)

with open(spacy_crime.csv_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        title = str(row["Title"])
        body = row["Body"]
        entities = spacy_crime.extract_entities(body)
        
        # Article contains a local location
        if entities["Location"]:
            try:
                cursor.execute("INSERT INTO articles (title) VALUES (?)", (title,))
                
                # Title is unique, insert related data
                cursor.execute("SELECT MAX(id) FROM articles")
                result = cursor.fetchone()
                if result[0] is not None:
                    cur_id = result[0] + 1
                else:
                    cur_id = 1
                
                insert_data(cursor, entities, cur_id)
            except sqlite3.IntegrityError as e:
                print(f"Constraint violation: {e}. Skipping article '{title}'.")
                continue

connection.commit()
connection.close()