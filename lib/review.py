import sqlite3
from lib import CONN, CURSOR

class Review:
    def __init__(self, year, summary, employee_id, id=None):
        self.year = year
        self.summary = summary
        self.employee_id = employee_id
        self.id = id

    def __repr__(self):
        return f"<Review(id={self.id}, year={self.year}, summary='{self.summary}', employee_id={self.employee_id})>"

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    summary TEXT NOT NULL,
                    employee_id INTEGER NOT NULL,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            ''')

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute('DROP TABLE IF EXISTS reviews')

    def save(self):
        with CONN:
            if self.id is None:
                CURSOR.execute('''
                    INSERT INTO reviews (year, summary, employee_id)
                    VALUES (?, ?, ?)
                ''', (self.year, self.summary, self.employee_id))
                self.id = CURSOR.lastrowid
            else:
                CURSOR.execute('''
                    UPDATE reviews
                    SET year = ?, summary = ?, employee_id = ?
                    WHERE id = ?
                ''', (self.year, self.summary, self.employee_id, self.id))
        
    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        id, year, summary, employee_id = row
        return cls(year, summary, employee_id, id)

    @classmethod
    def find_by_id(cls, id):
        with CONN:
            CURSOR.execute('SELECT * FROM reviews WHERE id = ?', (id,))
            row = CURSOR.fetchone()
            return cls.instance_from_db(row) if row else None

    def update(self):
        self.save()

    def delete(self):
        with CONN:
            CURSOR.execute('DELETE FROM reviews WHERE id = ?', (self.id,))
            self.id = None

    @classmethod
    def get_all(cls):
        with CONN:
            CURSOR.execute('SELECT * FROM reviews')
            rows = CURSOR.fetchall()
            return [cls.instance_from_db(row) for row in rows]
