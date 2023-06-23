import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from models import Character, Class, Race, Attribute, Skill, Spell, Equipment, CharacterAttribute, CharacterSkill, \
    CharacterSpell, CharacterEquipment, Spellcasting, engine
from sqlalchemy.orm import sessionmaker
from database import create_character, get_race_names, get_class_names

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()


class BaseWindow:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError("Subclasses must implement create_widgets method.")


class CharacterWindow(BaseWindow):

    def get_attributes(self):
        attributes = session.query(Attribute).all()
        return attributes
    def get_skills(self):
        skills = session.query(Skill).all()
        return skills
    def create_character(self):
        character_name = self.entry_name.get()
        class_name = self.combobox_class.get()
        race_name = self.combobox_race.get()
        background = self.entry_background.get()
        level = int(self.entry_level.get())
        exp = int(self.entry_exp.get())

        attributes_name = {}
        skills_name = {}
        for attribute_name, entry in self.attribute_entries.items():
            value = entry.get()
            attribute = session.query(Attribute).filter_by(attribute_name=attribute_name).first()
            attributes_name[attribute] = value
        for skill_name, entry in self.skill_entries.items():
            value = entry.get()
            skill = session.query(Skill).filter_by(skill_name=skill_name).first()
            skills_name[skill] = value
        selected_spells = [self.listbox_spells.get(idx) for idx in self.listbox_spells.curselection()]
        selected_equipment = [self.listbox_equipment.get(idx) for idx in self.listbox_equipment.curselection()]



        if create_character(character_name, class_name, race_name, background, level, exp, attributes_name,selected_spells, selected_equipment,skills_name,):

            messagebox.showinfo("Success", "Character created successfully.")
            refresh_character_list()
        else:
            messagebox.showerror("Error", "Failed to create character.")

    def create_widgets(self):
        self.label_name = tk.Label(self.root, text="Name:")
        self.entry_name = tk.Entry(self.root)

        self.label_class = tk.Label(self.root, text="Class:")
        self.combobox_class = ttk.Combobox(self.root, values=get_class_names())

        self.label_race = tk.Label(self.root, text="Race:")
        self.combobox_race = ttk.Combobox(self.root, values=get_race_names())

        self.label_background = tk.Label(self.root, text="Background:")
        self.entry_background = tk.Entry(self.root)

        self.label_level = tk.Label(self.root, text="Level:")
        self.entry_level = tk.Entry(self.root)

        self.label_exp = tk.Label(self.root, text="Experience:")
        self.entry_exp = tk.Entry(self.root)

        attributes = self.get_attributes()
        self.attribute_entries = {}

        for i in range(len(attributes)):
            label = tk.Label(self.root, text=f"{attributes[i].attribute_name}:")
            label.grid(row=i+1, column=2)
            entry = tk.Entry(self.root)
            entry.grid(row=i+1, column=3)

            self.attribute_entries[attributes[i].attribute_name] = entry

        self.label_spells = tk.Label(self.root, text="Spells:")
        self.listbox_spells = tk.Listbox(self.root, exportselection=False, selectmode=tk.MULTIPLE)
        self.scrollbar_spells = tk.Scrollbar(self.root, command=self.listbox_spells.yview)
        self.listbox_spells.config(yscrollcommand=self.scrollbar_spells.set)


        spells = session.query(Spell).all()
        for spell in spells:
            self.listbox_spells.insert(tk.END, spell.spell_name)

        self.label_equipment = tk.Label(self.root, text="Equipment:")
        self.listbox_equipment = tk.Listbox(self.root,exportselection=False, selectmode=tk.MULTIPLE)
        self.scrollbar_equipment = tk.Scrollbar(self.root, command=self.listbox_equipment.yview)
        self.listbox_equipment.config(yscrollcommand=self.scrollbar_equipment.set)

        equipment = session.query(Equipment).all()
        for equip in equipment:
            self.listbox_equipment.insert(tk.END, equip.equipment_name)

        skills = self.get_skills()
        self.skill_entries = {}

        row = 1
        column = 8
        for i in range(len(skills)):
            if row == 9:
                row = 1
                column += 2
            label = tk.Label(self.root, text=f"{skills[i].skill_name}:")
            label.grid(row=row, column=column, pady=0)
            entry = tk.Entry(self.root)
            entry.grid(row=row, column=column + 1, pady=0)
            row += 1

            self.skill_entries[skills[i].skill_name] = entry

        self.last_selected_spells = []
        self.last_selected_equipment = []

        self.button_create = tk.Button(
            self.root,
            text="Create Character",
            command=self.create_character,
        )
        self.create_layout()

    def create_layout(self):
        self.label_name.grid(row=1, column=0,pady=10)
        self.entry_name.grid(row=1, column=1,pady=10)
        self.label_class.grid(row=2, column=0,pady=10)
        self.combobox_class.grid(row=2, column=1,pady=10)
        self.label_race.grid(row=3, column=0,pady=10)
        self.combobox_race.grid(row=3, column=1,pady=10)
        self.label_background.grid(row=4, column=0,pady=10)
        self.entry_background.grid(row=4, column=1,pady=10)
        self.label_level.grid(row=5, column=0,pady=10)
        self.entry_level.grid(row=5, column=1,pady=10)
        self.label_exp.grid(row=6, column=0,pady=10)
        self.entry_exp.grid(row=6, column=1,pady=10)
        self.button_create.grid(row=8, column=4, pady=10)
        self.label_spells.grid(row=1, column=4, padx=10,)
        self.listbox_spells.grid(row=0, column=5,rowspan=8)
        self.label_equipment.grid(row=1, column=6, padx=10,)
        self.listbox_equipment.grid(row=0, column=7,rowspan=8)
        self.label_equipment.grid(row=1, column=6, padx=10,)
        self.listbox_equipment.grid(row=0, column=7,rowspan=8)




class CharacterEditWindow(BaseWindow):
    def __init__(self, root, character):
        self.character = character
        super().__init__(root, "Edit Character")

    def create_widgets(self):
        # Create labels and entry fields to edit character details
        self.label_name = tk.Label(self.root, text="Name:")
        self.entry_name = tk.Entry(self.root)
        self.entry_name.insert(END, self.character.character_name)

        self.label_class = tk.Label(self.root, text="Class:")
        self.combobox_class = ttk.Combobox(self.root, values=get_class_names())
        class_name = session.query(Class).filter_by(class_id=self.character.class_id).first().class_name
        self.combobox_class.insert(END, class_name)

        self.label_race = tk.Label(self.root, text="Race:")
        self.combobox_race = ttk.Combobox(self.root, values=get_race_names())
        race_name = session.query(Race).filter_by(race_id=self.character.race_id).first().race_name
        self.combobox_race.insert(END, race_name)

        self.label_background = tk.Label(self.root, text="Background:")
        self.entry_background = tk.Entry(self.root)
        self.entry_background.insert(END, self.character.background)

        self.label_level = tk.Label(self.root, text="Level:")
        self.entry_level = tk.Entry(self.root)
        self.entry_level.insert(END, self.character.level)

        self.label_exp = tk.Label(self.root, text="Experience:")
        self.entry_exp = tk.Entry(self.root)
        self.entry_exp.insert(END, self.character.exp)


        self.button_update = tk.Button(
            self.root,
            text="Update Character",
            command=self.update_character,
        )
        self.create_layout()

    def create_layout(self):
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
        self.button_update.pack()

    def update_character(self):
        class_id = session.query(Class).filter_by(class_name=self.combobox_class.get()).first().class_id
        race_id = session.query(Race).filter_by(race_name=self.combobox_race.get()).first().race_id
        # Update the character with the new values
        self.character.character_name = self.entry_name.get()
        self.character.class_id = class_id
        self.character.race_id = race_id
        self.character.background = self.entry_background.get()
        self.character.level = self.entry_level.get()
        self.character.exp = self.entry_exp.get()


        # Update other character attributes...

        session.commit()
        messagebox.showinfo("Success", "Character updated successfully.")
        self.root.destroy()


def refresh_character_list():
    characters = session.query(Character).all()
    listbox_characters.delete(0, END)
    for character in characters:
        listbox_characters.insert(END, character.character_name)


def refresh_spell_list():
    spells = session.query(Spell).all()
    listbox_spells(0, END)
    for spell in spells:
        listbox_spells.insert(END, spell.spell_name)


def refresh_equipment_list():
    equipment = session.query(Equipment).all()
    listbox_equipment.delete(0, END)
    for eq in equipment:
        listbox_equipment.insert(END, eq.equipment_name)


def delete_character():
    selected_index = listbox_characters.curselection()
    if selected_index:
        character_name = listbox_characters.get(selected_index)
        character = session.query(Character).filter_by(character_name=character_name).first()
        character_attribute = session.query(CharacterAttribute).filter_by(character_id=character.character_id).all()
        character_equipment = session.query(CharacterEquipment).filter_by(character_id=character.character_id).all()
        if character:
            for attribute in character_attribute:
                session.delete(attribute)
            for equipment in character_equipment:
                session.delete(equipment)
            session.delete(character)
            session.commit()
            refresh_character_list()
            info_text.delete('1.0', END)
            messagebox.showinfo("Success", "Character deleted successfully.")

def edit_character():
    selected_index = listbox_characters.curselection()
    if selected_index:
        character_name = listbox_characters.get(selected_index)
        character = session.query(Character).filter_by(character_name=character_name).first()
        if character:
            # Create an edit window or dialog to modify the character's details
            edit_window = Toplevel(root)
            edit_window.title("Edit Character")
            edit_form = CharacterEditWindow(edit_window, character)

def create_character_window():
    character_window = Toplevel(root)
    character_window.title("Create Character")
    character_form = CharacterWindow(character_window, "New character")

def open_character_edit_window(character):
    edit_window = Toplevel(root)
    edit_window.title("Edit Character")
    edit_form = CharacterEditWindow(edit_window, character)

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

            edit_button = tk.Button(root, text="Edit", command=lambda: open_character_edit_window(character))
            edit_button.place(relx=0.9, rely=0.1, anchor="ne")  # Position the button in the upper right corner


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


def show_spell_info(event):
    selected_index = listbox_spells.curselection()
    if selected_index:
        spell_name = listbox_spells.get(selected_index)
        spell = session.query(Spell).filter_by(spell_name=spell_name).first()
        if spell:
            spell_info_text.delete('1.0', END)
            spell_info_text.insert(END, f"ID: {spell.spell_id}\n")
            spell_info_text.insert(END, f"Name: {spell.spell_name}\n")
            spell_info_text.insert(END, f"Level: {spell.spell_level}\n")
            spell_info_text.insert(END, f"School: {spell.school}\n")
            spell_info_text.insert(END, f"Description: {spell.description}\n")


def show_equipment_info(event):
    selected_index = listbox_equipment.curselection()
    if selected_index:
        equipment_name = listbox_equipment.get(selected_index)
        equipment = session.query(Equipment).filter_by(equipment_name=equipment_name).first()
        if equipment:
            equipment_info_text.delete('1.0', END)
            equipment_info_text.insert(END, f"ID: {equipment.equipment_id}\n")
            equipment_info_text.insert(END, f"Name: {equipment.equipment_name}\n")
            equipment_info_text.insert(END, f"Weight: {equipment.weight}\n")
            equipment_info_text.insert(END, f"Cost: {equipment.cost}\n")


def refresh_spell_list():
    spells = session.query(Spell).all()
    listbox_spells.delete(0, END)
    for spell in spells:
        listbox_spells.insert(END, spell.spell_name)


def delete_spell():
    selected_index = listbox_spells.curselection()
    if selected_index:
        spell_name = listbox_spells.get(selected_index)
        spell = session.query(Spell).filter_by(spell_name=spell_name).first()
        if spell:
            session.delete(spell)
            session.commit()
            refresh_spell_list()
            info_text.delete('1.0', END)
            messagebox.showinfo("Success", "Spell deleted successfully.")


def delete_equipment():
    selected_index = listbox_equipment.curselection()
    if selected_index:
        equipment_name = listbox_equipment.get(selected_index)
        equipment = session.query(Equipment).filter_by(equipment_name=equipment_name).first()
        if equipment:
            session.delete(equipment)
            session.commit()
            refresh_spell_list()
            info_text.delete('1.0', END)
            messagebox.showinfo("Success", "Equipment deleted successfully.")


# Create the main window
root = tk.Tk()
root.title("DND Character Database")
# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the "Edit" menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Add options to the "Edit" menu
edit_menu.add_command(label="Edit Character", command=edit_character)
edit_menu.add_command(label="Delete Character", command=delete_character)
# Create a tabbed interface
tab_control = ttk.Notebook(root)

# Create the Characters tab
tab_characters = ttk.Frame(tab_control)
tab_control.add(tab_characters, text="Characters")

# Create a Listbox to display the characters
listbox_characters = tk.Listbox(tab_characters, width=20, height=20)
listbox_characters.grid(row=0, column=0, sticky="nsew")
listbox_characters.bind("<<ListboxSelect>>", show_character_info)

# Create a right-click menu for the listbox
listbox_menu = tk.Menu(root, tearoff=0)
listbox_menu.add_command(label="Delete", command=delete_character)


def show_listbox_menu(event):
    listbox_menu.post(event.x_root, event.y_root)


listbox_characters.bind("<Button-3>", show_listbox_menu)

# Create a frame for the character details
info_frame = tk.Frame(tab_characters)
info_frame.grid(row=0, column=1, sticky="nsew")

# Create a scrollbar for the character details
scrollbar = tk.Scrollbar(info_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

info_text = tk.Text(info_frame, yscrollcommand=scrollbar.set, width=50, height=20)
info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure grid weights to make the columns and rows expand and contract
tab_characters.grid_rowconfigure(0, weight=1)
tab_characters.grid_columnconfigure(1, weight=1)
info_frame.grid_rowconfigure(0, weight=1)
info_frame.grid_columnconfigure(0, weight=1)

# Configure the scrollbar to control the text widget
scrollbar.config(command=info_text.yview)

# Configure the scrollbar to control the text widget
scrollbar.config(command=info_text.yview)

# Add the tabbed interface to the root window
tab_control.pack(expand=True, fill=tk.BOTH)

# Create a button to open the character creation window
button_create_character = tk.Button(root, text="Create Character", command=create_character_window)
button_create_character.pack(pady=10)
# ...

# Create the Spells tab
tab_spells = ttk.Frame(tab_control)
tab_control.add(tab_spells, text="Spells")

# Create a Listbox to display the spells
listbox_spells = tk.Listbox(tab_spells, width=20, height=20)
listbox_spells.grid(row=0, column=0, sticky="nsew")
listbox_spells.bind("<<ListboxSelect>>", show_spell_info)

# Create a right-click menu for the spells listbox
spells_listbox_menu = tk.Menu(root, tearoff=0)
spells_listbox_menu.add_command(label="Delete", command=delete_spell)


def show_spells_listbox_menu(event):
    spells_listbox_menu.post(event.x_root, event.y_root)


listbox_spells.bind("<Button-3>", show_spells_listbox_menu)

# Create a frame for the spell details
spell_info_frame = tk.Frame(tab_spells)
spell_info_frame.grid(row=0, column=1, sticky="nsew")

# Create a scrollbar for the spell details
spell_scrollbar = tk.Scrollbar(spell_info_frame)
spell_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

spell_info_text = tk.Text(spell_info_frame, yscrollcommand=spell_scrollbar.set, width=50, height=20)
spell_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the grid weights for the Spells tab
tab_spells.grid_rowconfigure(0, weight=1)
tab_spells.grid_columnconfigure(1, weight=1)
spell_info_frame.grid_rowconfigure(0, weight=1)
spell_info_frame.grid_columnconfigure(0, weight=1)

# Create the Equipment tab
tab_equipment = ttk.Frame(tab_control)
tab_control.add(tab_equipment, text="Equipment")

# Create a Listbox to display the equipment
listbox_equipment = tk.Listbox(tab_equipment, width=20, height=20)
listbox_equipment.grid(row=0, column=0, sticky="nsew")
listbox_equipment.bind("<<ListboxSelect>>", show_equipment_info)

# Create a right-click menu for the equipment listbox
equipment_listbox_menu = tk.Menu(root, tearoff=0)
equipment_listbox_menu.add_command(label="Delete", command=delete_equipment)


def show_equipment_listbox_menu(event):
    equipment_listbox_menu.post(event.x_root, event.y_root)


listbox_equipment.bind("<Button-3>", show_equipment_listbox_menu)

# Create a frame for the equipment details
equipment_info_frame = tk.Frame(tab_equipment)
equipment_info_frame.grid(row=0, column=1, sticky="nsew")

# Create a scrollbar for the equipment details
equipment_scrollbar = tk.Scrollbar(equipment_info_frame)
equipment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

equipment_info_text = tk.Text(equipment_info_frame, yscrollcommand=equipment_scrollbar.set, width=50, height=20)
equipment_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the grid weights for the Equipment tab
tab_equipment.grid_rowconfigure(0, weight=1)
tab_equipment.grid_columnconfigure(1, weight=1)
equipment_info_frame.grid_rowconfigure(0, weight=1)
equipment_info_frame.grid_columnconfigure(0, weight=1)

refresh_character_list()
refresh_spell_list()
refresh_equipment_list()
root.mainloop()
