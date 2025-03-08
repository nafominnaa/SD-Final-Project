"""
Author: Anastasiia Fomina
Date Written: 2/21/2025
Assignment: Final Project
Description: Excavation company’s CRM (Customer Relationship Management)
"""
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage


# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('excavation_crm.db')
cursor = conn.cursor()

# Create database tables if they don't exist
def create_tables():
    """Creates necessary tables in the SQLite database."""
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
            description TEXT,
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
    """Adds a client to the database."""
    if not name or not contact_number or not email:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return
    cursor.execute('''
        INSERT INTO clients (name, contact_number, email)
        VALUES (?, ?, ?)
    ''', (name, contact_number, email))
    conn.commit()

# View Clients
def view_clients():
    """Displays a list of clients."""
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    return clients

# Job Management
def add_job(client_id, job_type, start_date, end_date):
    """Adds a job to the database."""
    if not job_type or not start_date or not end_date:
        messagebox.showerror("Input Error", "All job fields must be filled.")
        return
    cursor.execute('''
        INSERT INTO jobs (client_id, job_type, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (client_id, job_type, start_date, end_date, 'Scheduled'))
    conn.commit()

# Invoicing
def generate_invoice(job_id, amount, due_date, description):
    """Generates an invoice for a job."""
    if amount <= 0 or not due_date or not description:
        messagebox.showerror("Input Error", "Amount must be greater than zero, and all fields must be filled.")
        return
    cursor.execute('''
        INSERT INTO invoices (job_id, amount, due_date, description, paid)
        VALUES (?, ?, ?, ?, ?)
    ''', (job_id, amount, due_date, description, 0))  # Initially, not paid
    conn.commit()

# Time Tracking
def log_time(job_id, hours_worked):
    """Logs time worked for a job."""
    if hours_worked <= 0:
        messagebox.showerror("Input Error", "Hours worked must be greater than zero.")
        return
    cursor.execute('''
        INSERT INTO time_tracking (job_id, hours_worked, date_logged)
        VALUES (?, ?, ?)
    ''', (job_id, hours_worked, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

# -------------------------------
# GUI Setup
# -------------------------------

# Initialize Tkinter main window
root = tk.Tk()
root.title("Excavation CRM")

# Add images to the GUI
def load_image(image_path, alt_text):
    """Helper function to load images."""
    try:
        img = PhotoImage(file=image_path)
        return img
    except Exception as e:
        return alt_text

# First Window: Client Management
def client_management_window():
    """Window for client management."""
    client_win = tk.Toplevel(root)  # Creates a new top-level window
    client_win.title("Client Management")

    # Labels
    label_name = tk.Label(client_win, text="Client Name:")
    label_name.grid(row=0, column=0)
    label_contact = tk.Label(client_win, text="Contact Number:")
    label_contact.grid(row=1, column=0)
    label_email = tk.Label(client_win, text="Email:")
    label_email.grid(row=2, column=0)

    # Entry fields
    entry_name = tk.Entry(client_win)
    entry_name.grid(row=0, column=1)
    entry_contact = tk.Entry(client_win)
    entry_contact.grid(row=1, column=1)
    entry_email = tk.Entry(client_win)
    entry_email.grid(row=2, column=1)

    # Add client function with validation
    def add_client_callback():
        add_client(entry_name.get(), entry_contact.get(), entry_email.get())
        entry_name.delete(0, tk.END)
        entry_contact.delete(0, tk.END)
        entry_email.delete(0, tk.END)

    # Add Client button
    btn_add_client = tk.Button(client_win, text="Add Client", command=add_client_callback)
    btn_add_client.grid(row=3, column=0)

    # View Clients button
    def view_clients_callback():
        clients = view_clients()
        client_list = "\n".join([f"ID: {client[0]}, Name: {client[1]}, Contact: {client[2]}, Email: {client[3]}" for client in clients])
        messagebox.showinfo("Clients", client_list)

    btn_view_clients = tk.Button(client_win, text="View Clients", command=view_clients_callback)
    btn_view_clients.grid(row=3, column=1)

    # Close button
    btn_exit = tk.Button(client_win, text="Exit", command=client_win.destroy)
    btn_exit.grid(row=4, column=0, columnspan=2)

# Second Window: Job and Invoicing Management
def job_management_window():
    """Window for job scheduling and invoicing."""
    job_win = tk.Toplevel(root)  # Creates a new top-level window
    job_win.title("Job Management")

    # Labels for Job Entry
    label_job_type = tk.Label(job_win, text="Job Type:")
    label_job_type.grid(row=0, column=0)
    label_start_date = tk.Label(job_win, text="Start Date (YYYY-MM-DD):")
    label_start_date.grid(row=1, column=0)
    label_end_date = tk.Label(job_win, text="End Date (YYYY-MM-DD):")
    label_end_date.grid(row=2, column=0)

    # Entry fields for Job Entry
    entry_job_type = tk.Entry(job_win)
    entry_job_type.grid(row=0, column=1)
    entry_start_date = tk.Entry(job_win)
    entry_start_date.grid(row=1, column=1)
    entry_end_date = tk.Entry(job_win)
    entry_end_date.grid(row=2, column=1)

    # Add job function with validation
    def add_job_callback():
        client_id = 1  # Just an example, replace with actual client ID selection logic
        add_job(client_id, entry_job_type.get(), entry_start_date.get(), entry_end_date.get())
        entry_job_type.delete(0, tk.END)
        entry_start_date.delete(0, tk.END)
        entry_end_date.delete(0, tk.END)

    # Add Job button
    btn_add_job = tk.Button(job_win, text="Add Job", command=add_job_callback)
    btn_add_job.grid(row=3, column=0)

    # View Jobs button
    def view_jobs_callback():
        cursor.execute('SELECT * FROM jobs')
        jobs = cursor.fetchall()
        job_list = "\n".join([f"Job ID: {job[0]}, Client ID: {job[1]}, Type: {job[2]}, Start: {job[3]}, End: {job[4]}" for job in jobs])
        messagebox.showinfo("Jobs", job_list)

    btn_view_jobs = tk.Button(job_win, text="View Jobs", command=view_jobs_callback)
    btn_view_jobs.grid(row=3, column=1)

    # Labels for Invoice Generation
    label_amount = tk.Label(job_win, text="Amount ($):")
    label_amount.grid(row=4, column=0)
    label_due_date = tk.Label(job_win, text="Due Date (YYYY-MM-DD):")
    label_due_date.grid(row=5, column=0)
    label_description = tk.Label(job_win, text="Job Description:")
    label_description.grid(row=6, column=0)

    # Entry fields for Invoice Generation
    entry_amount = tk.Entry(job_win)
    entry_amount.grid(row=4, column=1)
    entry_due_date = tk.Entry(job_win)
    entry_due_date.grid(row=5, column=1)
    entry_description = tk.Entry(job_win)
    entry_description.grid(row=6, column=1)

    # Generate Invoice function
    def generate_invoice_callback():
        job_id = 1  # Example job ID, replace with actual selection logic
        generate_invoice(job_id, float(entry_amount.get()), entry_due_date.get(), entry_description.get())
        entry_amount.delete(0, tk.END)
        entry_due_date.delete(0, tk.END)
        entry_description.delete(0, tk.END)

    # Generate Invoice button
    btn_generate_invoice = tk.Button(job_win, text="Generate Invoice", command=generate_invoice_callback)
    btn_generate_invoice.grid(row=7, column=0)

    # View Invoices button
    def view_invoices_callback():
        cursor.execute('SELECT * FROM invoices')
        invoices = cursor.fetchall()
        invoice_list = "\n".join([f"Invoice ID: {invoice[0]}, Job ID: {invoice[1]}, Amount: {invoice[2]}, Due: {invoice[3]}, Description: {invoice[4]}" for invoice in invoices])
        messagebox.showinfo("Invoices", invoice_list)

    btn_view_invoices = tk.Button(job_win, text="View Invoices", command=view_invoices_callback)
    btn_view_invoices.grid(row=7, column=1)

    # Close button
    btn_exit = tk.Button(job_win, text="Exit", command=job_win.destroy)
    btn_exit.grid(row=8, column=0, columnspan=2)

# Main Menu
def main_menu():
    """Main menu window of the application."""
    # Labels
    label_title = tk.Label(root, text="Excavation CRM", font=("Helvetica", 16))
    label_title.grid(row=0, column=0, columnspan=2)

    # Buttons for navigation
    btn_client_management = tk.Button(root, text="Client Management", command=client_management_window)
    btn_client_management.grid(row=1, column=0)
    btn_job_management = tk.Button(root, text="Job Management", command=job_management_window)
    btn_job_management.grid(row=1, column=1)

    # Exit Button
    btn_exit = tk.Button(root, text="Exit", command=root.quit)
    btn_exit.grid(row=2, column=0, columnspan=2)

# Run the application
create_tables()
main_menu()

root.mainloop()
conn.close()