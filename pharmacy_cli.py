# pharmacy_cli.py
from tabulate import tabulate
from pharmacy_db_manager import PharmacyDBManager

class PharmacyCLI:
    def __init__(self):
        self.db_manager = PharmacyDBManager()

    def run(self):
        self.display_company_name()
        self.display_welcome_message()
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_medication()
            elif choice == "2":
                self.delete_medication()
            elif choice == "3":
                self.display_all_medications()
            elif choice == "4":
                self.create_patient()
            elif choice == "5":
                self.delete_patient()
            elif choice == "6":
                self.display_all_patients()
            elif choice == "7":
                self.create_prescription()
            elif choice == "8":
                self.delete_prescription()
            elif choice == "9":
                self.display_all_prescriptions()
            elif choice == "10":
                break
            else:
                print("Invalid choice. Please try again.")
            print("\n" * 3)  # Add space after displaying data

    def display_company_name(self):
        print("\nGETWELL PHARMACY")

    def display_welcome_message(self):
        print("Welcome to the Getwell Pharmacy. Please select a numbered choice to continue;")

    def display_menu(self):
        print("\nGetwell Main Menu")
        print("1. Add Medication")
        print("2. Delete Medication")
        print("3. Display All Medications")
        print("4. Add Patient")
        print("5. Delete Patient")
        print("6. Display All Patients")
        print("7. Add Prescription")
        print("8. Delete Prescription")
        print("9. Display All Prescriptions")
        print("10. Exit")
        print("\n" * 2)

    def create_medication(self):
        name = input("Enter medication name: ")
        medication_type = input("Enter medication type: ")
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
        if self.db_manager.check_medication_existence_by_name(name):
            print("Medication with this name already exists.")
            return
        self.db_manager.create_medication(name, medication_type, quantity, price)
        print("Medication added successfully.")

    def delete_medication(self):
        medications = self.db_manager.get_all_medications()
        headers = ["ID", "Name", "Type", "Quantity", "Price"]
        print(tabulate(medications, headers=headers))
        while True:
            medication_id = input("Enter medication ID to delete (Press Enter to exit): ")
            if not medication_id:
                return
            try:
                medication_id = int(medication_id)
                medication_name = self.db_manager.get_medication_name_by_id(medication_id)
                self.db_manager.delete_medication(medication_id)
                print(f"Medication '{medication_name}' deleted successfully.")
                break
            except ValueError:
                print("Invalid medication ID. Please try again.")

    def display_all_medications(self):
        medication_types = self.db_manager.get_medication_types()
        print("Available Medication Types:")
        print(", ".join(medication_types))
        medication_type = input("Enter medication type to display (Press Enter to display all types): ")
        medications = self.db_manager.get_all_medications()
        if medication_type:
            medications = [med for med in medications if med[4] == medication_type] 
        headers = ["ID", "Name", "Quantity", "Price", "Type"]
        print(tabulate(medications, headers=headers))

    def create_patient(self):
        name = input("Enter patient name: ")
        age = int(input("Enter patient age: "))
        address = input("Enter patient address (optional): ")
        if self.db_manager.check_patient_existence_by_name(name):
            print("Patient with this name already exists.")
            return
        self.db_manager.create_patient(name, age, address)
        print("Patient added successfully.")

    def delete_patient(self):
        patients = self.db_manager.get_all_patients()
        headers = ["ID", "Name", "Age", "Address"]
        print(tabulate(patients, headers=headers))
        while True:
            patient_id = input("Enter patient ID to delete (Press Enter to exit): ")
            if not patient_id:
                return
            try:
                patient_id = int(patient_id)
                patient_name = self.db_manager.get_patient_name_by_id(patient_id)
                self.db_manager.delete_patient(patient_id)
                print(f"Patient '{patient_name}' deleted successfully.")
                break
            except ValueError:
                print("Invalid patient ID. Please try again.")

    def display_all_patients(self):
        patients = self.db_manager.get_all_patients()
        headers = ["ID", "Name", "Age", "Address"]
        print(tabulate(patients, headers=headers))

    def create_prescription(self):
        medication_id = int(input("Enter medication ID: "))
        patient_id = int(input("Enter patient ID: "))
        dosage_instructions = input("Enter dosage instructions: ")
        self.db_manager.create_prescription(medication_id, patient_id, dosage_instructions)
        print("Prescription created successfully.")

    def delete_prescription(self):
        prescriptions = self.db_manager.get_all_prescriptions()
        headers = ["ID", "Medication Name", "Patient Name", "Dosage Instructions"]
        print(tabulate(prescriptions, headers=headers))
        while True:
            prescription_id = input("Enter prescription ID to delete (Press Enter to exit): ")
            if not prescription_id:
                return
            try:
                prescription_id = int(prescription_id)
                prescription = self.db_manager.get_prescription_by_id(prescription_id)
                medication_name = self.db_manager.get_medication_name_by_id(prescription[1])
                patient_name = self.db_manager.get_patient_name_by_id(prescription[2])
                self.db_manager.delete_prescription(prescription_id)
                print(f"Prescription for '{medication_name}' to '{patient_name}' deleted successfully.")
                break
            except ValueError:
                print("Invalid prescription ID. Please try again.")

    def display_all_prescriptions(self):
        prescriptions = self.db_manager.get_all_prescriptions()
        headers = ["ID", "Medication Name", "Patient Name", "Dosage Instructions"]
        prescriptions_with_names = []
        for prescription in prescriptions:
            medication_name = self.db_manager.get_medication_name_by_id(prescription[1])
            patient_name = self.db_manager.get_patient_name_by_id(prescription[2])
            prescriptions_with_names.append((prescription[0], medication_name, patient_name, prescription[3]))
        print(tabulate(prescriptions_with_names, headers=headers))

