from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Create the database engine
engine = create_engine('postgresql://postgres:timtim@localhost/DND')
# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()
# Create a base class for declarative models
Base = declarative_base()
# Define the Character model
class Character(Base):
    __tablename__ = 'characters'
    character_id = Column(Integer, primary_key=True)
    character_name = Column(String)
    class_id = Column(Integer, ForeignKey('classes.class_id'))
    race_id = Column(Integer, ForeignKey('races.race_id'))
    background = Column(String)
    level = Column(Integer)
    exp = Column(Integer)
    character_attribute = relationship("CharacterAttribute")
    character_skill = relationship("CharacterSkill")
    character_spell = relationship("CharacterSpell")
    character_equipment = relationship("CharacterEquipment")


# Define the Class model
class Class(Base):
    __tablename__ = 'classes'
    class_id = Column(Integer, primary_key=True)
    class_name = Column(String)
    hit_die = Column(String)
    primary_ability  = Column(Integer)
    spellcasting = relationship("Spellcasting")


# Define the Race model
class Race(Base):
    __tablename__ = 'races'
    race_id = Column(Integer, primary_key=True)
    race_name = Column(String)
    ability_bonuses = Column(String)
    speed = Column(Integer)


# Define the Attribute model
class Attribute(Base):
    __tablename__ = 'attribute'
    attribute_id = Column(Integer, primary_key=True)
    attribute_name = Column(String)


# Define the Skill model
class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String)
    attribute_id = Column(Integer, ForeignKey('attributes.id'))


# Define the Spell model
class Spell(Base):
    __tablename__ = 'spells'
    spell_id = Column(Integer, primary_key=True)
    spell_name = Column(String)
    spell_level = Column(Integer)
    school = Column(String)
    description = Column(String)


# Define the Equipment model
class Equipment(Base):
    __tablename__ = 'equipment'
    equipment_id = Column(Integer, primary_key=True)
    equipment_name = Column(String)
    weight = Column(Integer)
    cost = Column(Integer)


# Define the CharacterAttribute model
class CharacterAttribute(Base):
    __tablename__ = 'character_attribute'
    character_id = Column(Integer, ForeignKey('characters.character_id'), primary_key=True)
    attribute_id = Column(Integer, ForeignKey('attribute.attribute_id'), primary_key=True)
    value = Column(Integer)


# Define the CharacterSkill model
class CharacterSkill(Base):
    __tablename__ = 'character_skill'
    character_id = Column(Integer, ForeignKey('characters.character_id'), primary_key=True)
    skill_id = Column(Integer, ForeignKey('skills.skill_id'), primary_key=True)
    proficiency_level = Column(Integer)


# Define the CharacterSpell model
class CharacterSpell(Base):
    __tablename__ = 'character_spell'
    character_id = Column(Integer, ForeignKey('characters.character_id'), primary_key=True)
    spell_id = Column(Integer, ForeignKey('spells.spell_id'), primary_key=True)


# Define the CharacterEquipment model
class CharacterEquipment(Base):
    __tablename__ = 'character_equipment'
    character_id = Column(Integer, ForeignKey('characters.character_id'), primary_key=True)
    equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'), primary_key=True)
    quantity = Column(Integer)


# Define the Spellcasting model
class Spellcasting(Base):
    __tablename__ = 'spellcasting'
    spellcasting_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.class_id'))
    attribute_id = Column(Integer, ForeignKey('attributes.attributes_id'))
    spellcasting_modifier = Column(Integer)