import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#root@aryan#",
        database="hospital_db"
    )

# Global variable to track the selected item
selected_item = None

# Create a function to save hospital information
def save_hospital():
    reg_no = reg_no_entry.get()
    name = name_entry.get()
    rating = rating_entry.get()
    bed_capacity = bed_capacity_entry.get()
    num_doctors = num_doctors_entry.get()

    if reg_no and name and rating and bed_capacity and num_doctors:
        try:
            conn = connect_database()
            cursor = conn.cursor()
            query = "INSERT INTO hospitals (reg_no, name, rating, bed_capacity, num_doctors) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (reg_no, name, rating, bed_capacity, num_doctors))
            conn.commit()
            conn.close()

            # Add the hospital information to the Treeview
            tree.insert('', 'end', values=(reg_no, name, rating, bed_capacity, num_doctors))

            # Clear the input fields
            reg_no_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            rating_entry.delete(0, tk.END)
            bed_capacity_entry.delete(0, tk.END)
            num_doctors_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Hospital information saved successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Create a function to delete hospital information
def delete_hospital():
    global selected_item
    selected_item = tree.selection()[0]  # Get the selected item
    if selected_item:
        values = tree.item(selected_item, 'values')
        reg_no = values[0]
        try:
            conn = connect_database()
            cursor = conn.cursor()
            query = "DELETE FROM hospitals WHERE reg_no = %s"
            cursor.execute(query, (reg_no,))
            conn.commit()
            conn.close()

            # Remove the selected item from the Treeview
            tree.delete(selected_item)
            messagebox.showinfo("Success", "Selected hospital information deleted.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    else:
        messagebox.showerror("Error", "Please select a hospital to delete.")

# Create a function to search for hospital information
def search_hospital():
    search_text = search_entry.get()
    if search_text:
        try:
            conn = connect_database()
            cursor = conn.cursor()

            query = """
            SELECT * FROM hospitals 
            WHERE reg_no LIKE %s 
               OR name LIKE %s
               OR CAST(rating AS CHAR) LIKE %s 
               OR CAST(bed_capacity AS CHAR) LIKE %s 
               OR CAST(num_doctors AS CHAR) LIKE %s
            """

            search_query = f"%{search_text}%"
            cursor.execute(query, (search_query, search_query, search_query, search_query, search_query))

            results = cursor.fetchall()

            # Close the connection after fetching results
            conn.close()

            if results:
                tree.delete(*tree.get_children())
                for row in results:
                    tree.insert('', 'end', values=row)
            else:
                messagebox.showinfo("Search Result", "No matching hospital found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    else:
        messagebox.showerror("Error", "Please enter a search term.")

# Function to show all hospitals
def show_all_hospitals():
    load_data()  # Load all data from the database

# Create a function to update hospital information
def update_hospital():
    selected_items = tree.selection()
    if selected_items:
        selected_item = selected_items[0]  # Get the first selected item

        reg_no = reg_no_entry.get()
        name = name_entry.get()
        rating = rating_entry.get()
        bed_capacity = bed_capacity_entry.get()
        num_doctors = num_doctors_entry.get()

        if reg_no and name and rating and bed_capacity and num_doctors:
            try:
                conn = connect_database()
                cursor = conn.cursor()

                query = "UPDATE hospitals SET name = %s, rating = %s, bed_capacity = %s, num_doctors = %s WHERE reg_no = %s"
                cursor.execute(query, (name, rating, bed_capacity, num_doctors, reg_no))

                conn.commit()
                conn.close()

                tree.item(selected_item, values=(reg_no, name, rating, bed_capacity, num_doctors))

                messagebox.showinfo("Success", "Hospital information updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Please select a hospital to update.")

# Function to load data from the database
def load_data():
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospitals")
        results = cursor.fetchall()

        # Clear the Treeview before inserting new data
        tree.delete(*tree.get_children())

        for row in results:
            tree.insert('', 'end', values=row)
        
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Create the main window
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1050x600")

# Create and layout GUI components for hospital information
frame = tk.Frame(root, padx=20, pady=20, bg="#E6E6E6")
frame.pack(fill=tk.BOTH, expand=True)

# Labels and Entry Widgets for the Form
reg_no_label = tk.Label(frame, text="Registration No:", bg="#E6E6E6", font=("Arial", 14))
reg_no_label.grid(row=0, column=0, sticky="w")

reg_no_entry = tk.Entry(frame, font=("Arial", 12))
reg_no_entry.grid(row=0, column=1)

name_label = tk.Label(frame, text="Hospital Name:", bg="#E6E6E6", font=("Arial", 14))
name_label.grid(row=1, column=0, sticky="w")

name_entry = tk.Entry(frame, font=("Arial", 12))
name_entry.grid(row=1, column=1)

rating_label = tk.Label(frame, text="Rating:", bg="#E6E6E6", font=("Arial", 14))
rating_label.grid(row=2, column=0, sticky="w")

rating_entry = tk.Entry(frame, font=("Arial", 12))
rating_entry.grid(row=2, column=1)

bed_capacity_label = tk.Label(frame, text="Bed Capacity:", bg="#E6E6E6", font=("Arial", 14))
bed_capacity_label.grid(row=3, column=0, sticky="w")

bed_capacity_entry = tk.Entry(frame, font=("Arial", 12))
bed_capacity_entry.grid(row=3, column=1)

num_doctors_label = tk.Label(frame, text="No. of Doctors:", bg="#E6E6E6", font=("Arial", 14))
num_doctors_label.grid(row=4, column=0, sticky="w")

num_doctors_entry = tk.Entry(frame, font=("Arial", 12))
num_doctors_entry.grid(row=4, column=1)

# Create a Treeview to display the hospital information in a table
tree = ttk.Treeview(frame, columns=("Registration No", "Hospital Name", "Rating", "Bed Capacity", "No. of Doctors"), show="headings")
tree.grid(row=8, column=0, columnspan=2, pady=10)

# Define column headers
tree.heading("Registration No", text="Registration No")
tree.heading("Hospital Name", text="Hospital Name")
tree.heading("Rating", text="Rating")
tree.heading("Bed Capacity", text="Bed Capacity")
tree.heading("No. of Doctors", text="No. of Doctors")

# Create and layout buttons for various operations horizontally
button_frame = tk.Frame(frame, bg="#E6E6E6")
button_frame.grid(row=9, column=0, columnspan=2, pady=10)

save_button = tk.Button(button_frame, text="Add Data", command=save_hospital, bg="#4CAF50", fg="white", font=("Arial", 14))
save_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(button_frame, text="Delete Data", command=delete_hospital, bg="#FF5733", fg="white", font=("Arial", 14))
delete_button.grid(row=0, column=1, padx=5)

update_button = tk.Button(button_frame, text="Update Data", command=update_hospital, bg="#FFC300", fg="black", font=("Arial", 14))
update_button.grid(row=0, column=2, padx=5)

show_all_button = tk.Button(button_frame, text="Show All", command=show_all_hospitals, bg="#FFC300", fg="black", font=("Arial", 14))
show_all_button.grid(row=0, column=3, padx=5)

# Search label and entry
search_label = tk.Label(frame, text="Search:", bg="#E6E6E6", font=("Arial", 14))
search_label.grid(row=10, column=0, sticky="e")

search_entry = tk.Entry(frame, font=("Arial", 12))
search_entry.grid(row=10, column=1, sticky="w")

# Search button below all buttons
search_button = tk.Button(frame, text="Search", command=search_hospital, bg="#007BFF", fg="white", font=("Arial", 14))
search_button.grid(row=11, column=0, columnspan=2, pady=10)

# Load existing data into the Treeview
load_data()

# Start the Tkinter main loop
root.mainloop()
