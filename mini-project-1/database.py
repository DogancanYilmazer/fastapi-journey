from contextlib import contextmanager
import sqlite3


class Database:

    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                -- TODO: add your columns here, matching your Pydantic model fields
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                disease TEXT NOT NULL
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL
            )
        """)

    def get_all(self) -> list:
        self.cur.execute("SELECT * FROM patients")
        rows = self.cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get(self, id: int) -> dict | None:
        self.cur.execute("""
            SELECT * FROM patients WHERE id = ?
        """, (id,))
        row = self.cur.fetchone()
        return self._row_to_dict(row) if row else None

    def create(self, item) -> int:
        self.cur.execute("SELECT MAX(id) FROM patients")
        result = self.cur.fetchone()
        new_id = (result[0] or 0) + 1
        self.cur.execute("""
            INSERT INTO patients
            VALUES (:id, :name, :age, :disease)
        """, {"id": new_id, **item.model_dump()})
        self.conn.commit()
        return new_id

    def update(self, id: int, item) -> dict | None:
        self.cur.execute("""
            UPDATE patients
            SET name = :name, age = :age, disease = :disease
            WHERE id = :id
        """, {"id": id, **item.model_dump()})
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute("""
            DELETE FROM patients WHERE id = ?
        """, (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _row_to_dict(self, row) -> dict:
        # TODO: map each column position to its field name
        # Example: return {"id": row[0], "name": row[1], "age": row[2]}
        return {"id": row[0], "name": row[1], "age": row[2], "disease": row[3]}

    # Appointments methods
    def get_all_appointments(self) -> list:
        self.cur.execute("SELECT * FROM appointments")
        rows = self.cur.fetchall()
        return [self._appointment_row_to_dict(row) for row in rows]

    def get_appointment(self, id: int) -> dict | None:
        self.cur.execute("""
            SELECT * FROM appointments WHERE id = ?
        """, (id,))
        row = self.cur.fetchone()
        return self._appointment_row_to_dict(row) if row else None

    def create_appointment(self, item) -> int:
        self.cur.execute("SELECT MAX(id) FROM appointments")
        result = self.cur.fetchone()
        new_id = (result[0] or 0) + 1
        self.cur.execute("""
            INSERT INTO appointments
            VALUES (:id, :name, :date, :time)
        """, {"id": new_id, **item.model_dump()})
        self.conn.commit()
        return new_id

    def update_appointment(self, id: int, item) -> dict | None:
        self.cur.execute("""
            UPDATE appointments
            SET name = :name, date = :date, time = :time
            WHERE id = :id
        """, {"id": id, **item.model_dump()})
        self.conn.commit()
        return self.get_appointment(id)

    def delete_appointment(self, id: int):
        self.cur.execute("""
            DELETE FROM appointments WHERE id = ?
        """, (id,))
        self.conn.commit()

    def _appointment_row_to_dict(self, row) -> dict:
        return {"id": row[0], "name": row[1], "date": row[2], "time": row[3]}


@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()
    try:
        yield db
    finally:
        db.close()