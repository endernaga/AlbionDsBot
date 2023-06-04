from sqlalchemy import String, Text, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class BuildList(Base):
    __tablename__ = 'Список білдів'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), name='Назва білда', unique=True)
    description = Column(Text, name='Опис білда')
    profile_lists = relationship('ProfileList', secondary='Білди_до_активностів', backref='Список білдів')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class ProfileList(Base):
    __tablename__ = 'Список активностів'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), name='Назва активності', unique=True)
    description = Column(Text, name='Опис активності')
    build_lists = relationship('BuildList', secondary='Білди_до_активностів', backref='Список активностів')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class BuildToProfile(Base):
    __tablename__ = 'Білди_до_активностів'

    id = Column(Integer, primary_key=True)
    build_id = Column(Integer, ForeignKey('Список білдів.id'))
    profile_id = Column(Integer, ForeignKey('Список активностів.id'))
