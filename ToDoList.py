import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
from datetime import datetime
from tkinter import simpledialog
import time


# Function to connect to SQL Server
def connect_db():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=FAIQ-CH\\SQLEXPRESS;'
        'DATABASE=TaskManager;'
        'Trusted_Connection=yes;'
    )
    return conn


# Function to validate login credentials
def validate_login():
    username = username_entry.get() #admin
    password = password_entry.get() #admin123

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Username=? AND Password=?", username, password)
    user = cursor.fetchone()

    if user:
        login_window.destroy()
        open_task_manager()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")


# Function to open the main task manager window after login
def open_task_manager():
    global root, task_listbox  # Declare task_listbox as a global variable
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("600x600")
    root.config(bg="#F5F5DC")

    # Title Label
    title_label = tk.Label(root, text="To-Do List", font=("Arial", 24, "bold"), fg="#1E90FF", bg="#F5F5DC")
    title_label.pack(pady=10)

    # Task Entry Frame
    task_frame = tk.Frame(root, bg="#F5F5DC")
    task_frame.pack(pady=10)

    task_entry = tk.Entry(task_frame, width=30, font=("Arial", 14), bg="#FFFACD")
    task_entry.pack(side=tk.LEFT, padx=5)

    category_combobox = ttk.Combobox(task_frame, values=["Work", "Personal", "Urgent"], width=12, font=("Arial", 14))
    category_combobox.set("Work")
    category_combobox.pack(side=tk.LEFT, padx=5)

    priority_combobox = ttk.Combobox(task_frame, values=["Low", "Medium", "High"], width=10, font=("Arial", 14))
    priority_combobox.set("Medium")
    priority_combobox.pack(side=tk.LEFT, padx=5)

    add_button = tk.Button(
        task_frame, text="Add Task", command=lambda: add_task(task_entry, category_combobox, priority_combobox),
        font=("Arial", 12, "bold"), bg="#32CD32", fg="white", activebackground="#228B22"
    )
    add_button.pack(side=tk.LEFT)

    # Task Listbox
    task_listbox = tk.Listbox(root, width=50, height=15, font=("Arial", 12))
    task_listbox.pack(pady=10)

    # Buttons for additional features
    button_frame = tk.Frame(root, bg="#F5F5DC")
    button_frame.pack(pady=10)

    mark_completed_button = tk.Button(button_frame, text="Mark Completed", command=mark_completed,
                                      font=("Arial", 12, "bold"), bg="#FFD700")
    mark_completed_button.pack(side=tk.LEFT, padx=5)

    edit_button = tk.Button(button_frame, text="Edit Task", command=edit_task, font=("Arial", 12, "bold"), bg="#FF8C00")
    edit_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, font=("Arial", 12, "bold"),
                              bg="#DC143C")
    delete_button.pack(side=tk.LEFT, padx=5)

    filter_button = tk.Button(button_frame, text="Filter Pending", command=filter_pending, font=("Arial", 12, "bold"),
                              bg="#32CD32")
    filter_button.pack(side=tk.LEFT, padx=5)

    view_all_button = tk.Button(button_frame, text="View All Tasks", command=view_all_tasks, font=("Arial", 12, "bold"),
                                bg="#1E90FF")
    view_all_button.pack(side=tk.LEFT, padx=5)

    # Connect to the database
    global conn
    conn = connect_db()

    # Load all tasks when the application starts
    load_all_tasks()

    # Run the application
    root.mainloop()


# Function to add a task
def add_task(task_entry, category_combobox, priority_combobox):
    task = task_entry.get()
    category = category_combobox.get()
    priority = priority_combobox.get()

    if task.strip() and category.strip() and priority.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Tasks (Task, Category, Priority, Timestamp, Status) VALUES (?, ?, ?, ?, ?)",
            task, category, priority, timestamp, 'Pending'
        )
        conn.commit()
        task_listbox.insert(tk.END, f"{task} [{category}, {priority}]")
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "All fields must be filled!")


# Function to mark a task as completed
def mark_completed():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_name = task_listbox.get(selected_task_index)  # Get the task name
        task_listbox.delete(selected_task_index)  # Remove it from the listbox

        # Update the task status in the database to 'Completed'
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Tasks SET Status='Completed' WHERE Task=?", task_name
        )
        conn.commit()

        # Reinsert the task with the updated status into the Listbox
        task_listbox.insert(tk.END, f"{task_name} - Completed")
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as completed!")


# Function to edit a task
def edit_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        old_task = task_listbox.get(selected_task_index)
        new_task = simpledialog.askstring("Edit Task", f"Edit Task (Current: {old_task}):")
        if new_task:
            task_listbox.delete(selected_task_index)
            task_listbox.insert(tk.END, new_task)

            # Update the database with the edited task
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Tasks SET Task=? WHERE Task=?", new_task, old_task
            )
            conn.commit()
    else:
        messagebox.showwarning("Warning", "Please select a task to edit!")


# Function to delete a task
def delete_task():
    selected_task_index = task_listbox.curselection()  # Get selected task in Listbox
    if selected_task_index:
        task_name = task_listbox.get(selected_task_index)  # Get task name from the Listbox
        task_listbox.delete(selected_task_index)  # Remove the task from the Listbox

        # Delete the task from the database
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Tasks WHERE Task=?", task_name.split(' - ')[0])  # Only task name
        conn.commit()
    else:
        messagebox.showwarning("Warning", "Please select a task to delete!")


# Function to filter and show only pending tasks
def filter_pending():
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute("SELECT Task FROM Tasks WHERE Status='Pending'")
    tasks = cursor.fetchall()
    for task in tasks:
        task_listbox.insert(tk.END, task[0])


# Function to view all tasks (both completed and pending)
def view_all_tasks():
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute("SELECT Task, Status FROM Tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        task_listbox.insert(tk.END, f"{task[0]} - {task[1]}")


# Function to load all tasks initially when the application starts
def load_all_tasks():
    task_listbox.delete(0, tk.END)
    cursor = conn.cursor()
    cursor.execute("SELECT Task, Status FROM Tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        task_listbox.insert(tk.END, f"{task[0]} - {task[1]}")


# Function to close the login window and open the task manager
def open_task_manager_from_login():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login Page")
    login_window.geometry("400x300")

    # Username Label and Entry
    username_label = tk.Label(login_window, text="Username", font=("Arial", 14))
    username_label.pack(pady=5)

    global username_entry
    username_entry = tk.Entry(login_window, font=("Arial", 14))
    username_entry.pack(pady=5)

    # Password Label and Entry
    password_label = tk.Label(login_window, text="Password", font=("Arial", 14))
    password_label.pack(pady=5)

    global password_entry
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 14))
    password_entry.pack(pady=5)

    # Login Button
    login_button = tk.Button(
        login_window, text="Login", font=("Arial", 14), bg="#32CD32", fg="white", command=validate_login
    )
    login_button.pack(pady=10)

    # Start the login window
    login_window.mainloop()


# Connect to the database and start the application
conn = connect_db()
open_task_manager_from_login()
