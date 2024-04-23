import os
from datetime import datetime
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from perform_ocr import perform_ocr
from database import File, Tag, Category, load_database
from cluster import cluster_lda


def save_to_db(files):
    ocr_dict = perform_ocr(files)
    engine = load_database()

    with Session(engine) as session:
        document_term_matrix, feature_names, components = cluster_lda(ocr_dict)

        # Create files and tags
        tags = []

        for i in range(len(files)):
            file = File(file_path=files[i], text=ocr_dict[files[i]], date_added=datetime.today(), num_accesses=0)
            session.add(file)
            for j in document_term_matrix.getrow(i).indices:
                tag = Tag(description=feature_names[j])
                tags.append(tag)
                file.tags.append(tag)
        session.add_all(tags)

        # Create categories and add tags to categories
        categories = [Category(name=f'Category {i + 1}') for i in range(len(components))]
        session.add_all(categories)

        # Extract topics. Inspired by:
        # https://stackoverflow.com/questions/44208501/getting-topic-word-distribution-from-lda-in-scikit-learn
        words_per_topic = 10

        for topic_index, component in enumerate(components):
            word_indexes = component.argsort()[::-1][:words_per_topic]
            for i in word_indexes:
                tags[i].categories.append(categories[topic_index])

        session.commit()


def retrieve_files():
    engine = load_database()

    with Session(engine) as session:
        statement = select(File)
        files = session.scalars(statement).fetchmany(size=8)
        print(files)
        return get_json_for_files(files)


def retrieve_categories():
    engine = load_database()

    with Session(engine) as session:
        statement = select(Category)
        categories = session.scalars(statement).all()
        json_data = []

        for category in categories:
            category_data = {}
            category_data['name'] = category.name
            json_data.append(category_data)

    return json_data


def retrieve_files_by_category(category_id):
    engine = load_database()

    with Session(engine) as session:
        statement = select(Tag.id).join(Category.tags).where(Category.id == category_id)
        print(statement)
        tag_ids = session.scalars(statement).all()
        print(tag_ids)
        statement = select(File).join(Tag.files).filter(Tag.id.in_(tag_ids)).distinct()
        files = session.scalars(statement).all()
        print([(file.id, file.file_path) for file in files])
        return get_json_for_files(files)


# Retrieves json data from a series of File objects
def get_json_for_files(files):
    json_data = []

    for file in files:
        file_data = {}
        file_data['hoverText'] = file.text
        file_data['title'] = Path(file.file_path).stem
        file_data['imagePath'] = file.file_path
        json_data.append(file_data)

    return json_data
