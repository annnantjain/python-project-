# 🏥 Hospital Management System

A desktop Hospital Management System built with **Python**, **Tkinter**, and **SQLite3**. It provides a clean, tabbed interface to manage hospital records, doctors, patient appointments, and billing with live statistical dashboards and search capabilities.

---

## 🌟 Features

- **📊 Live Dashboard**:
  - Real-time counters for Total Patients, Total Doctors, and Total Appointments.
  - Live revenue calculation from billing records.
- **👨‍⚕️ Doctor Management**:
  - Add, update, view, search, and delete doctor profiles.
  - Track specialization, contact details, and availability status.
- **🧑‍🤝‍🧑 Patient Management**:
  - Record patient personal details (Name, Age, Gender, Phone, Address).
  - Validation ensures valid age and positive numeric values.
- **📅 Appointment Scheduling**:
  - Schedule patient appointments with specific doctors, dates, times, and reasons.
  - Track appointment statuses (`Scheduled`, `Completed`, `Cancelled`).
  - Strict date format validation (`YYYY-MM-DD`).
- **💳 Billing & Invoicing**:
  - Generate patient bills with custom amounts and payment statuses (`Paid`, `Pending`).
  - Real-time updates to hospital revenue metrics upon payment.
- **🔍 Universal Search**:
  - Search across all fields in any tab with partial keyword matching.
- **💾 Local SQLite Database**:
  - Automatically initializes and manages `hospital.db` in the application directory.

---

## 📁 Project Structure

```
hospital-management-system/
│
├── app.py              # Main Tkinter application & SQLite database logic
├── requirements.txt    # Project dependencies (built-in standard library)
├── .gitignore          # Git ignore configuration
├── README.md           # Documentation
└── tests/
    └── test_app.py     # Automated unit test suite
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed on your machine.
- Tkinter (included by default with standard Python on Windows and macOS).
  - *On Linux (Ubuntu/Debian):* install via `sudo apt-get install python3-tk`.

### Running the Application

1. Clone or download this repository:
   ```bash
   git clone https://github.com/annnantjain/hospital-management-system.git
   cd hospital-management-system
   ```

2. Run the application:
   ```bash
   python app.py
   ```

### Running Automated Tests

Run the test suite using Python's built-in `unittest` runner:
```bash
python -m unittest tests/test_app.py
```

---

## 🛠️ Database Schema

The SQLite database (`hospital.db`) contains four tables:

1. **`patients`**:
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `name`: TEXT NOT NULL
   - `age`: INTEGER
   - `gender`: TEXT
   - `phone`: TEXT
   - `address`: TEXT

2. **`doctors`**:
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `name`: TEXT NOT NULL
   - `specialization`: TEXT
   - `phone`: TEXT
   - `availability`: TEXT

3. **`appointments`**:
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `patient`: TEXT
   - `doctor`: TEXT
   - `date`: TEXT
   - `time`: TEXT
   - `reason`: TEXT
   - `status`: TEXT

4. **`bills`**:
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `patient`: TEXT
   - `amount`: REAL
   - `date`: TEXT
   - `payment_status`: TEXT

---

## 📝 License
This project is open source and available under the [MIT License](LICENSE).
