from models import Character, Class, Race, Attribute, Skill, Spell, Equipment, CharacterAttribute, CharacterSkill, CharacterSpell, CharacterEquipment, Spellcasting, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Session = sessionmaker(bind=engine)

def create_character(character_name, class_name, race_name, background, level, exp,attribute_names, selected_spells, selected_equipment,skills_names):
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
            attributes = attribute_names.items()
            for pairs in attributes:
                character_attribute = CharacterAttribute(character_id=character.character_id,
                                                         attribute_id=pairs[0].attribute_id, value=pairs[1])
                session.add(character_attribute)
            session.commit()

            skill = skills_names.items()
            for pairs in skill:
                if pairs[1]:
                    character_skill = CharacterSkill(character_id=character.character_id,
                                                             skill_id=pairs[0].skill_id,proficiency_level=pairs[1])
                    session.add(character_skill)
            session.commit()
            if len(selected_spells) > 0:
                for spell_name in selected_spells:
                    spell = session.query(Spell).filter_by(spell_name=spell_name).first()
                    character_spell = CharacterSpell(
                        character_id=character.character_id,
                        spell_id = spell.spell_id,
                        spellcasting_id=session.query(Spellcasting).filter_by(class_id=character.class_id).first().spellcasting_id
                    )
                    session.add(character_spell)
                session.commit()
            if len(selected_equipment) > 0:
                for equip_name in selected_equipment:
                    equip = session.query(Equipment).filter_by(equipment_name=equip_name).first()
                    character_equip = CharacterEquipment(
                        character_id=character.character_id,
                        equipment_id=equip.equipment_id,
                        quantity=1
                    )
                    session.add(character_equip)
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
