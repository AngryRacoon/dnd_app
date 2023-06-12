from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

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

Base.metadata.create_all(engine)
class CharacterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("DND Character Database")

        self.label_name = Label(self.root, text="Name:")
        self.entry_name = Entry(self.root)

        self.label_class = Label(self.root, text="Class:")
        self.combobox_class = ttk.Combobox(self.root, values=self.get_class_names())

        self.label_race = Label(self.root, text="Race:")
        self.combobox_race = ttk.Combobox(self.root, values=self.get_race_names())

        self.label_background = Label(self.root, text="Background:")
        self.entry_background = Entry(self.root)

        self.label_level = Label(self.root, text="Level:")
        self.entry_level = Entry(self.root)

        self.label_exp = Label(self.root, text="Experience:")
        self.entry_exp = Entry(self.root)

        self.button_create = Button(
            self.root,
            text="Create Character",
            command=self.create_character
        )

        self.button_create.pack()
        self.label_name.pack()
        self.entry_name.pack()
        self.label_class.pack()
        self.combobox_class.pack()
        self.label_race.pack()
        self.combobox_race.pack()
        self.label_background.pack()
        self.entry_background.pack()
        self.label_level.pack()
        self.entry_level.pack()
        self.label_exp.pack()
        self.entry_exp.pack()

    def get_class_names(self):
        classes = session.query(Class).all()
        return [class_obj.class_name for class_obj in classes]

    def get_race_names(self):
        races = session.query(Race).all()
        return [race_obj.race_name for race_obj in races]

    def create_character(self):
        character_name = self.entry_name.get()
        class_name = self.combobox_class.get()
        race_name = self.combobox_race.get()
        background = self.entry_background.get()
        level = int(self.entry_level.get())
        exp = int(self.entry_exp.get())

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

        try:
            session.add(character)
            session.commit()
            messagebox.showinfo("Success", "Character created successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))

def refresh_character_list():
    characters = session.query(Character).all()
    listbox_characters.delete(0, END)
    for character in characters:
        listbox_characters.insert(END, character.character_name)
def refresh_spell_list():
    spells = session.query(Spell).all()
    listbox_characters.delete(0, END)
    for spell in spells:
        listbox_characters.insert(END, spell.spell_name)
def refresh_equipment_list():
    equipment = session.query(Equipment).all()
    listbox_characters.delete(0, END)
    for eq in equipment:
        listbox_characters.insert(END, eq.equipment_name)

def delete_character():
    selected_index = listbox_characters.curselection()
    if selected_index:
        character_name = listbox_characters.get(selected_index)
        character = session.query(Character).filter_by(character_name=character_name).first()
        if character:
            session.delete(character)
            session.commit()
            refresh_character_list()
            info_text.delete('1.0', END)
            messagebox.showinfo("Success", "Character deleted successfully.")

def show_character_info(event):
    selected_index = listbox_characters.curselection()
    if selected_index:
        character_name = listbox_characters.get(selected_index)
        character = session.query(Character).filter_by(character_name=character_name).first()
        if character:
            info_text.delete('1.0', END)
            info_text.insert(END, f"Name: {character.character_name}\n")
            class_name = session.query(Class).filter_by(class_id=character.class_id).first().class_name
            info_text.insert(END, f"Class: {class_name}\n")
            race_name = session.query(Race).filter_by(race_id=character.race_id).first().race_name
            info_text.insert(END, f"Race: {race_name}\n")
            info_text.insert(END, f"Background: {character.background}\n")
            info_text.insert(END, f"Level: {character.level}\n")
            info_text.insert(END, f"Experience: {character.exp}\n\n")

            # Query and display additional details
            skills = session.query(Skill, CharacterSkill).filter(
                CharacterSkill.character_id == character.character_id,
                Skill.skill_id == CharacterSkill.skill_id
            ).all()
            if skills:
                info_text.insert(END, "Skills:\n")
                for skill, char_skill in skills:
                    info_text.insert(END, f"- {skill.skill_name}: {char_skill.proficiency_level}\n")

            attributes = session.query(Attribute, CharacterAttribute).filter(
                CharacterAttribute.character_id == character.character_id,
                Attribute.attribute_id == CharacterAttribute.attribute_id
            ).all()
            if attributes:
                info_text.insert(END, "\nAttributes:\n")
                for attribute, char_attribute in attributes:
                    info_text.insert(END, f"- {attribute.attribute_name}: {char_attribute.value}\n")


            equipment = session.query(Equipment, CharacterEquipment).filter(
                CharacterEquipment.character_id == character.character_id,
                Equipment.equipment_id == CharacterEquipment.equipment_id
            ).all()
            if equipment:
                info_text.insert(END, "Equipment:\n")
                for eq, char_eq in equipment:
                    info_text.insert(END, f"- {eq.equipment_name}: {char_eq.quantity}\n")

            spells = session.query(Spell).join(CharacterSpell).filter(
                CharacterSpell.character_id == character.character_id).all()
            if spells:
                info_text.insert(END, "Spells:\n")
                for spell in spells:
                    info_text.insert(END, f"- {spell.spell_name}\n")
def create_character_window():
    character_window = Toplevel(root)
    character_window.title("Create Character")
    character_form = CharacterWindow(character_window)

# Create the main window
root = Tk()
root.title("DND Character Database")

# Create a Listbox to display the characters
listbox_characters = Listbox(root, width=20, height=20)
listbox_characters.grid(row=0, column=0, sticky="nsew")
listbox_characters.bind("<<ListboxSelect>>", show_character_info)

# Create a right-click menu for the listbox
listbox_menu = Menu(root, tearoff=0)
listbox_menu.add_command(label="Delete", command=delete_character)

def show_listbox_menu(event):
    listbox_menu.post(event.x_root, event.y_root)

listbox_characters.bind("<Button-3>", show_listbox_menu)

# Create a frame for the character details
info_frame = Frame(root)
info_frame.grid(row=0, column=1, sticky="nsew")

# Create a scrollbar for the character details
scrollbar = Scrollbar(info_frame)
scrollbar.pack(side=RIGHT, fill=Y)

info_text = Text(info_frame, yscrollcommand=scrollbar.set, width=50, height=20)
info_text.pack(side=LEFT, fill=BOTH, expand=True)

# Configure grid weights to make the columns and rows expand and contract
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
info_frame.grid_rowconfigure(0, weight=1)
info_frame.grid_columnconfigure(0, weight=1)

# Configure the scrollbar to control the text widget
scrollbar.config(command=info_text.yview)

# Create a button to open the character creation window
button_create_character = Button(root, text="Create Character", command=create_character_window)
button_create_character.grid(row=1, column=0, columnspan=2, pady=10)

# Refresh the character list on startup
refresh_character_list()

# Start the main event loop
root.mainloop()

