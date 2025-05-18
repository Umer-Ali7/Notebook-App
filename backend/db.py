import sqlite3
from datetime import datetime

DB_NAME = "notes.db"

class NoteDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.init_db()

    def init_db(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                created_at TEXT,
                tags TEXT,
                reminder_date TEXT
            )
        ''')
        self.conn.commit()

    def add_note(self, title, content, tags, reminder_date):
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO notes (title, content, created_at, tags, reminder_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tags, reminder_date))
        self.conn.commit()

    def get_notes(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM notes ORDER BY created_at DESC')
        return c.fetchall()

    def delete_note(self, note_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM notes WHERE id=?', (note_id,))
        self.conn.commit()

    def search_notes(self, keyword):
        c = self.conn.cursor()
        c.execute('''
            SELECT * FROM notes
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{keyword}%', f'%{keyword}%'))
        return c.fetchall()



# Image wala system me add nhi kr raha mene remove kar dia ab tum muje ek readme.md file bana ke do ji me code e features batane he sir ne kaha tha



# -----------------------------------------------------






# from datetime import datetime
# import json

# class Note:
#     def __init__(self, title, content, tags=None, reminder_date=None):
#         self.title = title
#         self.content = content
#         self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.tags = tags or []
#         self.reminder_date = reminder_date

#     def to_dict(self):
#         return {
#                 "title": self.title,
#                 "content": self.content,
#                 "created_at": self.created_at,
#                 "tags": self.tags,
#                 "reminder_date": self.reminder_date
#         }
        
# class Notebook:
#     def __init__(self):
#         self.notes = []

#     def add_note(self, note):
#         self.notes.append(note)

#     def delete_note(self, title):
#         self.notes = [n for n in self.notes if n.title != title]

#     def get_all_notes(self):
#         return self.notes
    
#     def search_notes(self, keyword):
#         return [note for note in self.notes if keyword.lower() in note.title.lower() or keyword.lower() in note.content.lower()]

    
#     def save_to_file(self, filename = "notes.json"):
#         with open(filename, "w") as f:
#             json.dump([note.to_dict() for note in self.notes], f, indent=4)

#     def load_from_file(self, filename = "notes.json"):
#         try:
#             with open(filename, "r") as f:
#                 notes_data = json.load(f)
#                 self.notes = [Note(d["title"], d["content"], d.get("tags"), d.get("reminder_date")) for d in notes_data]
#         except FileNotFoundError:
#             self.notes = []