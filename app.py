import os
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    address TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    phone TEXT,
    availability TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient TEXT,
    doctor TEXT,
    date TEXT,
    time TEXT,
    reason TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient TEXT,
    amount REAL,
    date TEXT,
    payment_status TEXT
)
""")

conn.commit()


# ==========================================
# 2. MAIN APPLICATION
# ==========================================

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1200x750")
root.minsize(1000, 650)
root.configure(bg="#edf2f7")


# ==========================================
# 3. STYLING
# ==========================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#263445",
    rowheight=30,
    fieldbackground="white",
    font=("Arial", 10),
)

style.configure(
    "Treeview.Heading",
    background="#234b70",
    foreground="white",
    font=("Arial", 10, "bold"),
)

style.configure(
    "TNotebook.Tab",
    font=("Arial", 11, "bold"),
    padding=[15, 10],
)

style.map("Treeview", background=[("selected", "#b8d8f0")])


# ==========================================
# 4. HEADER
# ==========================================

header = tk.Frame(root, bg="#163a5f", height=75)
header.pack(fill="x")

tk.Label(
    header,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 23, "bold"),
    fg="white",
    bg="#163a5f",
).pack(pady=18)


# ==========================================
# 5. DASHBOARD
# ==========================================

dashboard = tk.Frame(root, bg="#edf2f7")
dashboard.pack(fill="x", padx=20, pady=15)

tk.Label(
    dashboard,
    text="Hospital Overview",
    font=("Arial", 18, "bold"),
    bg="#edf2f7",
    fg="#163a5f",
).pack(anchor="w", pady=10)

stats_frame = tk.Frame(dashboard, bg="#edf2f7")
stats_frame.pack(fill="x")


def get_count(table):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]


def get_revenue():
    cursor.execute("SELECT SUM(amount) FROM bills")
    row = cursor.fetchone()
    return row[0] if (row and row[0] is not None) else 0.0


stat_labels = {}


def create_stat_card(title, key):
    card = tk.Frame(
        stats_frame,
        bg="white",
        bd=1,
        relief="solid",
        padx=20,
        pady=15,
    )

    card.pack(side="left", fill="both", expand=True, padx=8)

    tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg="white",
        fg="#64748b",
    ).pack()

    value = tk.Label(
        card,
        text="0",
        font=("Arial", 23, "bold"),
        bg="white",
        fg="#163a5f",
    )

    value.pack(pady=8)
    stat_labels[key] = value


create_stat_card("Total Patients", "patients")
create_stat_card("Total Doctors", "doctors")
create_stat_card("Appointments", "appointments")
create_stat_card("Total Revenue", "revenue")


def update_dashboard():
    stat_labels["patients"].config(text=str(get_count("patients")))
    stat_labels["doctors"].config(text=str(get_count("doctors")))
    stat_labels["appointments"].config(text=str(get_count("appointments")))
    stat_labels["revenue"].config(text=f"Rs. {get_revenue():.2f}")


# ==========================================
# 6. TAB SYSTEM
# ==========================================

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=10)


# ==========================================
# 7. GENERIC MANAGEMENT MODULE
# ==========================================

class ManagementPage:

    def __init__(self, parent, table, columns, fields,
                 title, required_fields):

        self.table = table
        self.columns = columns
        self.fields = fields
        self.required_fields = required_fields
        self.entries = {}

        self.frame = tk.Frame(parent, bg="#edf2f7")

        parent.add(self.frame, text=title)

        self.create_form()
        self.create_table()
        self.refresh()

    # --------------------------------------
    # CREATE INPUT FORM
    # --------------------------------------

    def create_form(self):

        form = tk.LabelFrame(
            self.frame,
            text="Enter Information",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=15,
        )

        form.pack(fill="x", padx=15, pady=10)

        for index, field in enumerate(self.fields):

            row = index // 3
            col = (index % 3) * 2

            tk.Label(
                form,
                text=field + ":",
                bg="white",
                font=("Arial", 10, "bold"),
            ).grid(
                row=row,
                column=col,
                padx=8,
                pady=10,
                sticky="w",
            )

            if field in ["Gender", "Status", "Availability",
                         "Payment Status"]:

                options = {
                    "Gender": ["Male", "Female", "Other"],
                    "Status": ["Scheduled", "Completed", "Cancelled"],
                    "Availability": ["Available", "Unavailable"],
                    "Payment Status": ["Paid", "Pending"],
                }

                entry = ttk.Combobox(
                    form,
                    values=options[field],
                    state="readonly",
                    width=20,
                )

                entry.set(options[field][0])

            else:

                entry = tk.Entry(
                    form,
                    font=("Arial", 10),
                    width=23,
                )

            entry.grid(
                row=row,
                column=col + 1,
                padx=8,
                pady=10,
            )

            self.entries[field] = entry

        # BUTTONS

        button_frame = tk.Frame(form, bg="white")
        button_frame.grid(
            row=(len(self.fields) + 2) // 3,
            column=0,
            columnspan=6,
            pady=15,
        )

        buttons = [
            ("Add Record", self.add_record),
            ("Update Record", self.update_record),
            ("Delete Record", self.delete_record),
            ("Clear Fields", self.clear_fields),
        ]

        for text, command in buttons:

            tk.Button(
                button_frame,
                text=text,
                command=command,
                bg="#234b70",
                fg="white",
                font=("Arial", 9, "bold"),
                padx=12,
                pady=7,
                cursor="hand2",
            ).pack(side="left", padx=6)

    # --------------------------------------
    # CREATE RECORD TABLE
    # --------------------------------------

    def create_table(self):

        search_frame = tk.Frame(
            self.frame,
            bg="#edf2f7",
        )

        search_frame.pack(fill="x", padx=15, pady=8)

        tk.Label(
            search_frame,
            text="Search:",
            bg="#edf2f7",
            font=("Arial", 11, "bold"),
        ).pack(side="left", padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=30,
            font=("Arial", 11),
        )

        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_records,
            bg="#16805d",
            fg="white",
            padx=12,
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.refresh,
            bg="#64748b",
            fg="white",
            padx=12,
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.frame)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10,
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings",
        )

        for column in self.columns:

            self.tree.heading(
                column,
                text=column,
            )

            self.tree.column(
                column,
                width=130,
                anchor="center",
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set,
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_record,
        )

    # --------------------------------------
    # GET FORM DATA
    # --------------------------------------

    def get_values(self):

        return [
            self.entries[field].get().strip()
            for field in self.fields
        ]

    # --------------------------------------
    # VALIDATE INPUTS
    # --------------------------------------

    def validate_inputs(self):

        for field in self.required_fields:
            if not self.entries[field].get().strip():
                raise ValueError(f"Please enter {field}.")

        if self.table == "patients":
            age = self.entries["Age"].get().strip()
            if age:
                try:
                    age_int = int(age)
                    if age_int <= 0 or age_int > 130:
                        raise ValueError("Age must be between 1 and 130.")
                except ValueError as e:
                    if "between" in str(e):
                        raise e
                    raise ValueError("Age must be a valid positive integer.")

        if self.table == "appointments":
            date_str = self.entries["Date"].get().strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format (e.g., 2026-12-01).")

        if self.table == "bills":
            amount_str = self.entries["Amount"].get().strip()
            try:
                amount = float(amount_str)
                if amount < 0:
                    raise ValueError("Amount cannot be negative.")
            except ValueError as e:
                if "negative" in str(e):
                    raise e
                raise ValueError("Amount must be a valid number.")

    # --------------------------------------
    # ADD NEW RECORD
    # --------------------------------------

    def add_record(self):

        try:
            self.validate_inputs()
            values = self.get_values()

            placeholders = ", ".join(["?"] * len(self.fields))
            field_names = ", ".join(
                f'"{field.lower().replace(" ", "_")}"'
                for field in self.fields
            )

            cursor.execute(
                f"INSERT INTO {self.table} ({field_names}) "
                f"VALUES ({placeholders})",
                values,
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Record added successfully!",
            )

            self.refresh()
            self.clear_fields()
            update_dashboard()

        except ValueError as error:

            messagebox.showwarning(
                "Invalid Input",
                str(error),
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
            )

    # --------------------------------------
    # SELECT RECORD
    # --------------------------------------

    def select_record(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        for index, field in enumerate(self.fields):

            entry = self.entries[field]
            val = str(values[index + 1]) if (index + 1 < len(values) and values[index + 1] is not None) else ""

            if isinstance(entry, ttk.Combobox):
                entry.set(val)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, val)

    # --------------------------------------
    # UPDATE RECORD
    # --------------------------------------

    def update_record(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Required",
                "Select a record to update.",
            )
            return

        try:
            self.validate_inputs()
            values = self.get_values()

            record_id = self.tree.item(selected[0])["values"][0]

            assignments = ", ".join(
                f'"{field.lower().replace(" ", "_")}" = ?'
                for field in self.fields
            )

            cursor.execute(
                f"UPDATE {self.table} SET {assignments} "
                "WHERE id = ?",
                values + [record_id],
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Record updated successfully!",
            )

            self.refresh()
            self.clear_fields()
            update_dashboard()

        except ValueError as error:

            messagebox.showwarning(
                "Invalid Input",
                str(error),
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
            )

    # --------------------------------------
    # DELETE RECORD
    # --------------------------------------

    def delete_record(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Required",
                "Select a record to delete.",
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?",
        )

        if confirm:

            record_id = self.tree.item(selected[0])["values"][0]

            cursor.execute(
                f"DELETE FROM {self.table} WHERE id = ?",
                (record_id,),
            )

            conn.commit()

            messagebox.showinfo(
                "Deleted",
                "Record deleted successfully!",
            )

            self.refresh()
            self.clear_fields()
            update_dashboard()

    # --------------------------------------
    # SEARCH RECORDS
    # --------------------------------------

    def search_records(self):

        keyword = self.search_entry.get().strip()

        if not keyword:
            self.refresh()
            return

        self.tree.delete(*self.tree.get_children())

        # Match SQLite table columns formatted as lowercase with underscores
        db_columns = [col.lower().replace(" ", "_") for col in self.columns]

        conditions = " OR ".join(
            [f'CAST("{col}" AS TEXT) LIKE ?'
             for col in db_columns]
        )

        parameters = [f"%{keyword}%"] * len(db_columns)

        cursor.execute(
            f"SELECT * FROM {self.table} "
            f"WHERE {conditions}",
            parameters,
        )

        for record in cursor.fetchall():

            self.tree.insert(
                "",
                tk.END,
                values=record,
            )

    # --------------------------------------
    # REFRESH TABLE
    # --------------------------------------

    def refresh(self):

        self.tree.delete(*self.tree.get_children())

        cursor.execute(f"SELECT * FROM {self.table}")

        for record in cursor.fetchall():

            self.tree.insert(
                "",
                tk.END,
                values=record,
            )

    # --------------------------------------
    # CLEAR INPUT FIELDS
    # --------------------------------------

    def clear_fields(self):

        for field in self.fields:

            entry = self.entries[field]

            if isinstance(entry, ttk.Combobox):

                entry.current(0)

            else:

                entry.delete(0, tk.END)

        # Clear selection on treeview
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)


# ==========================================
# 8. CREATE ALL MANAGEMENT MODULES
# ==========================================

patients_page = ManagementPage(
    notebook,
    "patients",
    ("ID", "Name", "Age", "Gender", "Phone", "Address"),
    ["Name", "Age", "Gender", "Phone", "Address"],
    "Patients",
    ["Name"],
)

doctors_page = ManagementPage(
    notebook,
    "doctors",
    ("ID", "Name", "Specialization", "Phone", "Availability"),
    ["Name", "Specialization", "Phone", "Availability"],
    "Doctors",
    ["Name"],
)

appointments_page = ManagementPage(
    notebook,
    "appointments",
    ("ID", "Patient", "Doctor", "Date", "Time", "Reason", "Status"),
    ["Patient", "Doctor", "Date", "Time", "Reason", "Status"],
    "Appointments",
    ["Patient", "Doctor", "Date"],
)

billing_page = ManagementPage(
    notebook,
    "bills",
    ("ID", "Patient", "Amount", "Date", "Payment Status"),
    ["Patient", "Amount", "Date", "Payment Status"],
    "Billing",
    ["Patient", "Amount", "Date"],
)


# ==========================================
# 9. FOOTER
# ==========================================

footer = tk.Frame(
    root,
    bg="#163a5f",
    height=35,
)

footer.pack(fill="x", side="bottom")

tk.Label(
    footer,
    text="Hospital Management System | Python + Tkinter + SQLite",
    font=("Arial", 9),
    bg="#163a5f",
    fg="white",
).pack(pady=8)


# ==========================================
# 10. START APPLICATION
# ==========================================

update_dashboard()


def close_application():
    conn.close()
    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_application,
)


if __name__ == "__main__":
    root.mainloop()
