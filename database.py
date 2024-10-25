from peewee import *
import os


db = PostgresqlDatabase(
    os.getenv('POSTGRES_DB'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    autorollback=True
)

class Category(Model):
    id = AutoField()
    name = CharField()
    parent = ForeignKeyField('self', null=True, backref='subcategories')

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Category])

if __name__ == '__main__':
    create_tables()