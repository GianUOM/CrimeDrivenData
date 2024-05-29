Malta CrimeDB already includes the necessary data for it to function, you can simply run backend.py to start the Flask application.

If you wish to scrape and create the database from scratch:
    Ensure that the chromedriver appropriate to your browser version is in the root directory of the project
    Run tom_scraper.py to start scraping from the Times of Malta
    Run dbs.py to create the database locally