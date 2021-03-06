from flask import Flask
from flask.cli import AppGroup
from faker import Faker


from app.models.authors_model import AuthorModel
from app.models.authors_products_model import AuthorsProducts

from app.services.products_services import ProductServices

import json


def init_app(app):

    cli_db_group = AppGroup('database')

    @cli_db_group.command('create_books')
    def cli_db_create_all_books():
        print('*CREATING DATABASES IF NOT EXISTS*')

        fake = Faker()
        session = app.db.session

        print('*POPULATING DATABASES BOOKS AUTHORS*')
        with open('books.json', 'r') as books_data:
            products = dict(json.load(books_data))

            for book in products.get('books'):
                new_author = AuthorModel(
                    name=fake.name(),
                    birthplace=fake.address()
                )
                session.add(new_author)
                session.commit()

                ProductServices(session).create_book(book, new_author.id)

    @cli_db_group.command('create')
    def cli_db_create_all():
        app.db.create_all()

    @cli_db_group.command('drop')
    def cli_db_drop_all():
        app.db.drop_all()

    app.cli.add_command(cli_db_group)
