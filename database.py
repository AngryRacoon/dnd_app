from models import Character, Class, Race, Attribute, Skill, Spell, Equipment, CharacterAttribute, CharacterSkill, CharacterSpell, CharacterEquipment, Spellcasting, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Session = sessionmaker(bind=engine)

def create_character(character_name, class_name, race_name, background, level, exp):
    try:
        with Session() as session:
            # Get the class and race IDs based on the selected names
            class_id = session.query(Class).filter_by(class_name=class_name).first().class_id
            race_id = session.query(Race).filter_by(race_name=race_name).first().race_id

            # Create a new Character instance
            character = Character(
                character_name=character_name,
                class_id=class_id,
                race_id=race_id,
                background=background,
                level=level,
                exp=exp
            )

            session.add(character)
            session.commit()

            return True
    except SQLAlchemyError:
        return False


def get_class_names():
    with Session() as session:
        class_names = [c.class_name for c in session.query(Class).all()]
    return class_names
def get_race_names():
    with Session() as session:
        race_names = [r.race_name for r in session.query(Race).all()]
    return race_names
