import sqlite3
from datetime import datetime
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('excavation_crm.db')
cursor = conn.cursor()
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact_number TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            job_type TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(client_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            amount REAL,
            due_date TEXT,
            paid INTEGER,
            FOREIGN KEY(job_id) REFERENCES jobs(job_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_tracking (
            time_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            hours_worked REAL,
            date_logged TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(job_id)
        )
    ''')
    conn.commit()
# Client Management
def add_client(name, contact_number, email):
    cursor.execute('''
        INSERT INTO clients (name, contact_number, email)
        VALUES (?, ?, ?)
    ''', (name, contact_number, email))
    conn.commit()
def view_clients():
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    print("\nClients List:")
    for client in clients:
        print(f"ID: {client[0]}, Name: {client[1]}, Contact: {client[2]}, Email: {client[3]}")
# Job Scheduling
def add_job(client_id, job_type, start_date, end_date):
    cursor.execute('''
        INSERT INTO jobs (client_id, job_type, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (client_id, job_type, start_date, end_date, 'Scheduled'))
    conn.commit()
def view_jobs():
    cursor.execute('SELECT * FROM jobs')
    jobs = cursor.fetchall()
    print("\nJobs List:")
    for job in jobs:
        print(f"Job ID: {job[0]}, Client ID: {job[1]}, Job Type: {job[2]}, Start Date: {job[3]}, End Date: {job[4]}, Status: {job[5]}")
# Invoicing and Billing
def generate_invoice(job_id, amount, due_date):
    cursor.execute('''
        INSERT INTO invoices (job_id, amount, due_date, paid)
        VALUES (?, ?, ?, ?)
    ''', (job_id, amount, due_date, 0))  # Initially, not paid
    conn.commit()
def view_invoices():
    cursor.execute('SELECT * FROM invoices')
    invoices = cursor.fetchall()
    print("\nInvoices List:")
    for invoice in invoices:
        paid_status = "Paid" if invoice[4] == 1 else "Unpaid"
        print(f"Invoice ID: {invoice[0]}, Job ID: {invoice[1]}, Amount: ${invoice[2]}, Due Date: {invoice[3]}, Status: {paid_status}")
def mark_invoice_as_paid(invoice_id):
    cursor.execute('''
        UPDATE invoices
        SET paid = 1
        WHERE invoice_id = ?
    ''', (invoice_id,))
    conn.commit()
# Time Tracking
def log_time(job_id, hours_worked):
    cursor.execute('''
        INSERT INTO time_tracking (job_id, hours_worked, date_logged)
        VALUES (?, ?, ?)
    ''', (job_id, hours_worked, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
def view_time_tracking():
    cursor.execute('SELECT * FROM time_tracking')
    time_entries = cursor.fetchall()
    print("\nTime Tracking Log:")
    for entry in time_entries:
        print(f"Time ID: {entry[0]}, Job ID: {entry[1]}, Hours Worked: {entry[2]}, Date Logged: {entry[3]}")
# Main Menu
def main_menu():
    while True:
        print("\nExcavation CRM Menu:")
        print("1. Add Client")
        print("2. View Clients")
        print("3. Add Job")
        print("4. View Jobs")
        print("5. Generate Invoice")
        print("6. View Invoices")
        print("7. Mark Invoice as Paid")
        print("8. Log Time Worked")
        print("9. View Time Tracking")
        print("0. Exit") 
        choice = input("Choose an option: ")
        if choice == '1':
            name = input("Enter client name: ")
            contact_number = input("Enter client contact number: ")
            email = input("Enter client email: ")
            add_client(name, contact_number, email)
        elif choice == '2':
            view_clients()
        elif choice == '3':
            view_clients()
            client_id = int(input("Enter client ID: "))
            job_type = input("Enter job type: ")
            start_date = input("Enter job start date (YYYY-MM-DD): ")
            end_date = input("Enter job end date (YYYY-MM-DD): ")
            add_job(client_id, job_type, start_date, end_date)
        elif choice == '4':
            view_jobs()
        elif choice == '5':
            view_jobs()
            job_id = int(input("Enter job ID for the invoice: "))
            amount = float(input("Enter amount for the invoice: "))
            due_date = input("Enter due date for the invoice (YYYY-MM-DD): ")
            generate_invoice(job_id, amount, due_date)
        elif choice == '6':
            view_invoices()
        elif choice == '7':
            view_invoices()
            invoice_id = int(input("Enter invoice ID to mark as paid: "))
            mark_invoice_as_paid(invoice_id)
        elif choice == '8':
            view_jobs()
            job_id = int(input("Enter job ID to log time for: "))
            hours_worked = float(input("Enter number of hours worked: "))
            log_time(job_id, hours_worked)
        elif choice == '9':
            view_time_tracking()
        elif choice == '0':
            print("Exiting CRM...")
            break
        else:
            print("Invalid option. Please try again.")
if __name__ == "__main__":
    create_tables()
    main_menu()
    conn.close()