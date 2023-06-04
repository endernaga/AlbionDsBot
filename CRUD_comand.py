from model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def create_object(object, dbname='test.sqlite', **kwargs):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        ses.add(object(**kwargs))
        return ses.commit()


def read_object(object, object_id=0, dbname='test.sqlite'):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        if object_id == 0:
            return ses.query(object).all()
        else:
            return ses.query(object).where(object.id == object_id).one()


def update_object(object, object_id: int, dbname='test.sqlite', **kwargs):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        ses.query(object).where(object.id == object_id).update(kwargs)
        return ses.commit()


def delete_object(object, object_id: int, dbname='test.sqlite'):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        ses.query(object).where(object.id == object_id).delete()
        return ses.commit()


if __name__ == '__main__':
    pass