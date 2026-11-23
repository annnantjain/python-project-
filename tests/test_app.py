import os
import sys
import unittest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Suppress messageboxes during automated testing
import tkinter.messagebox as mb
mb.showinfo = lambda *args, **kwargs: None
mb.showwarning = lambda *args, **kwargs: None
mb.showerror = lambda *args, **kwargs: None
mb.askyesno = lambda *args, **kwargs: True

import app

class TestHospitalManagementSystem(unittest.TestCase):

    def setUp(self):
        # Clear tables before each test
        for table in ["patients", "doctors", "appointments", "bills"]:
            app.cursor.execute(f"DELETE FROM {table}")
        app.conn.commit()
        app.update_dashboard()

    def test_patients_crud_and_combobox(self):
        # 1. Add patient
        app.patients_page.entries["Name"].delete(0, 'end')
        app.patients_page.entries["Name"].insert(0, "Jane Doe")
        app.patients_page.entries["Age"].delete(0, 'end')
        app.patients_page.entries["Age"].insert(0, "32")
        app.patients_page.entries["Gender"].set("Female")
        app.patients_page.entries["Phone"].delete(0, 'end')
        app.patients_page.entries["Phone"].insert(0, "1234567890")
        app.patients_page.entries["Address"].delete(0, 'end')
        app.patients_page.entries["Address"].insert(0, "456 Elm St")
        app.patients_page.add_record()

        app.cursor.execute("SELECT name, gender, age FROM patients WHERE name = 'Jane Doe'")
        record = app.cursor.fetchone()
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "Jane Doe")
        self.assertEqual(record[1], "Female")
        self.assertEqual(record[2], 32)

        # 2. Select patient from Treeview
        children = app.patients_page.tree.get_children()
        self.assertTrue(len(children) > 0)
        app.patients_page.tree.selection_set(children[0])
        app.patients_page.select_record()

        # Combobox should be updated to "Female"
        self.assertEqual(app.patients_page.entries["Gender"].get(), "Female")

        # 3. Update patient
        app.patients_page.entries["Age"].delete(0, 'end')
        app.patients_page.entries["Age"].insert(0, "33")
        app.patients_page.update_record()

        app.cursor.execute("SELECT age FROM patients WHERE name = 'Jane Doe'")
        self.assertEqual(app.cursor.fetchone()[0], 33)

        # 4. Search patient
        app.patients_page.search_entry.delete(0, 'end')
        app.patients_page.search_entry.insert(0, "Jane")
        app.patients_page.search_records()
        self.assertEqual(len(app.patients_page.tree.get_children()), 1)

    def test_billing_and_multiword_search(self):
        # Add bill
        app.billing_page.entries["Patient"].delete(0, 'end')
        app.billing_page.entries["Patient"].insert(0, "John Doe")
        app.billing_page.entries["Amount"].delete(0, 'end')
        app.billing_page.entries["Amount"].insert(0, "500.00")
        app.billing_page.entries["Date"].delete(0, 'end')
        app.billing_page.entries["Date"].insert(0, "2026-11-23")
        app.billing_page.entries["Payment Status"].set("Paid")
        app.billing_page.add_record()

        # Search by Payment Status "Paid"
        app.billing_page.search_entry.delete(0, 'end')
        app.billing_page.search_entry.insert(0, "Paid")
        app.billing_page.search_records()
        results = app.billing_page.tree.get_children()
        self.assertEqual(len(results), 1, "Searching by Payment Status 'Paid' failed")

    def test_dashboard_metrics(self):
        # Insert test records
        app.cursor.execute("INSERT INTO patients (name, age, gender) VALUES ('Bob', 40, 'Male')")
        app.cursor.execute("INSERT INTO doctors (name, specialization) VALUES ('Dr. House', 'Diagnostics')")
        app.cursor.execute("INSERT INTO appointments (patient, doctor, date) VALUES ('Bob', 'Dr. House', '2026-12-01')")
        app.cursor.execute("INSERT INTO bills (patient, amount, payment_status) VALUES ('Bob', 1200.0, 'Paid')")
        app.conn.commit()

        app.update_dashboard()
        self.assertEqual(app.stat_labels["patients"].cget("text"), "1")
        self.assertEqual(app.stat_labels["doctors"].cget("text"), "1")
        self.assertEqual(app.stat_labels["appointments"].cget("text"), "1")
        self.assertIn("1200.00", app.stat_labels["revenue"].cget("text"))

    @classmethod
    def tearDownClass(cls):
        app.close_application()

if __name__ == "__main__":
    unittest.main()
