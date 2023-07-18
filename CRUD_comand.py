import model
from model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

dbname = 'test.sqlite'
def create_object(object, dbname=dbname, **kwargs):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        ses.add(object(**kwargs))
        return ses.commit()


def read_object(object, object_id=0, dbname=dbname):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        if object_id == 0:
            return ses.query(object).all()
        else:
            return ses.query(object).where(object.id == object_id).one()


def update_object(object, object_id: int, dbname=dbname, **kwargs):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        if 'build_lists' in kwargs:
            ses.query(object).where(object.id == object_id).one().build_lists = []
            ses.query(object).where(object.id == object_id).one().build_lists = kwargs['build_lists']
            del kwargs['build_lists']
            if len(kwargs) == 0:
                return ses.commit()
        ses.query(object).where(object.id == object_id).update(kwargs)
        return ses.commit()


def delete_object(object, object_id: int, dbname=dbname):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        ses.query(object).where(object.id == object_id).delete()
        return ses.commit()


def get_builds(profile:model.ProfileList):
    engine = create_engine(f'sqlite:///{dbname}')
    with Session(bind=engine) as ses:
        if profile not in ses:
            profile = ses.query(ProfileList).get(profile.id)
        print(profile.build_lists)
        return profile.build_lists


if __name__ == '__main__':
    print(read_object(ProfileList, object_id=1))
    update_object(ProfileList, 2, build_lists=[read_object(BuildList, object_id=3)])
    engine = create_engine(f'sqlite:///{dbname}')
    #with Session(bind=engine) as ses:
        #ses.query(ProfileList).where(ProfileList.id == 2).one().build_lists = [read_object(BuildList, object_id=2)]
        #ses.commit()