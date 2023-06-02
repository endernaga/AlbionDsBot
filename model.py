from sqlalchemy import String, Text, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class BuildList(Base):
    __tablename__ = 'Список білдів'

    id = Column(Integer ,primary_key=True)
    name = Column(String(30), name='Назва білда', unique=True)
    description = Column(Text, name='Опис білда')
    profile_lists = relationship('ProfileList', secondary='Білди до активностів', back_populates='Список білдів')


class ProfileList(Base):
    __tablename__ = 'Список активностів'

    id = Column(Integer ,primary_key=True)
    name = Column(String(30), name='Назва активності', unique=True)
    description = Column(Text, name='Опис активності')
    build_lists = relationship('BuildList', secondary='Білди до активностів', back_populates='Список активностів')

class BuildToProfile(Base):
    __tablename__ = 'Білди до активностів'

    id = Column(Integer, primary_key=True)
    build_id = Column(Integer, ForeignKey('Список білдів.id'))
    profile_id = Column(Integer, ForeignKey('Список активностів.id'))
