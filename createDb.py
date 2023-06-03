from sqlalchemy import create_engine

from model import Base


def create_db(name:str, dbname):
    engine = create_engine(f'sqlite:///{name}')
    dbname.metadata.create_all(engine)


if __name__ == '__main__':
    create_db('test.sqlite', Base)