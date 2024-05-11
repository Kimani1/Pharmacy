import sqlite3

class PharmacyDBManager:
    def __init__(self):
        self.connection = sqlite3.connect('pharmacy.db')
        self.cursor = self.connection.cursor()

        # Create tables if they don't exist
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS medications (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                type TEXT NOT NULL,
                                quantity INTEGER NOT NULL,
                                price REAL NOT NULL
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                age INTEGER NOT NULL,
                                address TEXT
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
                                id INTEGER PRIMARY KEY,
                                medication_id INTEGER NOT NULL,
                                patient_id INTEGER NOT NULL,
                                dosage_instructions TEXT,
                                FOREIGN KEY (medication_id) REFERENCES medications(id),
                                FOREIGN KEY (patient_id) REFERENCES patients(id)
                            )''')

    def create_medication(self, name, medication_type, quantity, price):
        self.cursor.execute('''INSERT INTO medications (name, type, quantity, price) 
                               VALUES (?, ?, ?, ?)''', (name, medication_type, quantity, price))
        self.connection.commit()

    def delete_medication(self, medication_id):
        self.cursor.execute('''DELETE FROM medications WHERE id = ?''', (medication_id,))
        self.connection.commit()

    def get_all_medications(self):
        self.cursor.execute('''SELECT * FROM medications''')
        return self.cursor.fetchall()

    def get_medications_by_type(self, medication_type):
        if medication_type:
            self.cursor.execute('''SELECT * FROM medications WHERE type = ?''', (medication_type,))
        else:
            self.cursor.execute('''SELECT * FROM medications''')
        return self.cursor.fetchall()

    def get_medication_types(self):
        self.cursor.execute('''SELECT DISTINCT type FROM medications''')
        return [row[0] for row in self.cursor.fetchall()]

    def check_medication_existence_by_name(self, name):
        self.cursor.execute('''SELECT * FROM medications WHERE name = ?''', (name,))
        return bool(self.cursor.fetchone())

    def create_patient(self, name, age, address=None):
        self.cursor.execute('''INSERT INTO patients (name, age, address) 
                               VALUES (?, ?, ?)''', (name, age, address))
        self.connection.commit()

    def check_patient_existence_by_name(self, name):
        self.cursor.execute('''SELECT * FROM patients WHERE name = ?''', (name,))
        return bool(self.cursor.fetchone())

    def delete_patient(self, patient_id):
        self.cursor.execute('''DELETE FROM patients WHERE id = ?''', (patient_id,))
        self.connection.commit()

    def get_all_patients(self):
        self.cursor.execute('''SELECT * FROM patients''')
        return self.cursor.fetchall()

    def create_prescription(self, medication_id, patient_id, dosage_instructions):
        self.cursor.execute('''INSERT INTO prescriptions (medication_id, patient_id, dosage_instructions) 
                               VALUES (?, ?, ?)''', (medication_id, patient_id, dosage_instructions))
        self.connection.commit()

    def delete_prescription(self, prescription_id):
        self.cursor.execute('''DELETE FROM prescriptions WHERE id = ?''', (prescription_id,))
        self.connection.commit()

    def get_all_prescriptions(self):
        self.cursor.execute('''SELECT * FROM prescriptions''')
        return self.cursor.fetchall()

    def get_medication_name_by_id(self, medication_id):
        self.cursor.execute('''SELECT name FROM medications WHERE id = ?''', (medication_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_patient_name_by_id(self, patient_id):
        self.cursor.execute('''SELECT name FROM patients WHERE id = ?''', (patient_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_prescription_by_id(self, prescription_id):
        self.cursor.execute('''SELECT * FROM prescriptions WHERE id = ?''', (prescription_id,))
        return self.cursor.fetchone()
