import os
import json

import flask
from flask import Flask, request, make_response
from flask_cors import CORS
from database import create_database
from database_ops import save_to_db, retrieve_files, retrieve_categories, retrieve_files_by_category

app = Flask(
    __name__
)

CORS(app)

# Set up database
#database = Database('declutter')
#reate_tables()
#database.create_table('master', ('id', 'name', 'title', 'text', 'image'))


@app.route('/')
def hello():
    # Wipe JSON storage file if it exists
    open('file_paths.json', 'w')

    create_database()
    return 'The power of the sun in the palm of my hand!'


@app.route('/add-files', methods=['POST'])
def add_files():
    file_paths = request.json
    with open('file_paths.json', 'w') as file:
        json.dump(file_paths, file)
    return 'success!'


@app.route('/save-files', methods=['GET'])
def save_files():
    with open('file_paths.json', 'r+') as file:
        save_to_db(json.load(file))
        file.truncate(0)
    return 'success!'


@app.route('/files')
def get_files():
    return retrieve_files()


@app.route('/categories')
def get_categories():
    return retrieve_categories()


@app.route('/files-by-category', methods=['POST'])
def get_files_by_category():
    category_id = request.json
    return retrieve_files_by_category(category_id)


@app.route('/search', methods=['POST'])
def get_search_results():
    search_term = request.json


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
