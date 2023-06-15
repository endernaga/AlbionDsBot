from sqlalchemy import String, Text, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase): # клас пустишка , для наслідування
    pass


class BuildList(Base):
    __tablename__ = 'Список білдів'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), name='Назва білда', unique=True)
    description = Column(Text, name='Опис білда')
    role = Column(String(30), name='Позиція', default='RDD')
    profile_lists = relationship('ProfileList', secondary='Білди_до_активностів', backref='Список білдів')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class ProfileList(Base):# зробити к-сть танків , хілів, дд , рдд
    __tablename__ = 'Список активностів'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), name='Назва активності', unique=True)
    description = Column(Text, name='Опис активності')
    tank_count = Column(Integer, default=0, name='Число танків')
    heal_count = Column(Integer, default=0, name='Число хілів')
    support_count = Column(Integer, default=0, name='Число сапортів')
    mdd_count = Column(Integer, default=0, name='Число МДД')
    rdd_count = Column(Integer, default=0, name='Число РДД')
    battle_mount_count = Column(Integer, default=0, name='Число батл маунтів')
    build_lists = relationship('BuildList', secondary='Білди_до_активностів', backref='Список активностів')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class BuildToProfile(Base): # 3-тя бд для того щоб зробити звязок багато до багато
    __tablename__ = 'Білди_до_активностів'

    id = Column(Integer, primary_key=True)
    build_id = Column(Integer, ForeignKey('Список білдів.id'))
    profile_id = Column(Integer, ForeignKey('Список активностів.id'))
