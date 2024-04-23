import os
from sqlalchemy import select
from sqlalchemy.orm import Session
from database_ops import save_to_db, retrieve_files_by_category
from database import File, Tag, Category, load_database


def get_file_paths(directory):
    file_paths = []

    # Walk through all files in the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file_name in files:
            # Join the directory path with the file name
            file_path = os.path.join(root, file_name)
            # Add the file path to the list
            file_paths.append(file_path)

    return file_paths


def test_save_to_db():
    print('starting test')
    file_paths = get_file_paths('test_files')
    save_to_db(file_paths)


def test_retrieve_data():
    engine = load_database()

    data_to_select = [File, Category]

    with Session(engine) as session:
        for data_class in data_to_select:
            statement = select(data_class)
            data = session.scalars(statement).all()
            for datum in data:
                print(datum)


def test_retrieve_files_for_category():
    retrieve_files_by_category(10)
