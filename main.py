import sqlite3
import tkinter.messagebox as MessageBox
from tkinter import *
from tkinter import ttk

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute(
  '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)'''
)
conn.commit()

# Tkinter GUI
root = Tk()
root.title("Student List")
root.geometry("800x600")


# Function to create a new user
def create_user():
  id = id_entry.get()
  name = name_entry.get()
  age = age_entry.get()
  cursor.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
                 (id, name, age))
  conn.commit()
  id_entry.delete(0, END)
  name_entry.delete(0, END)
  age_entry.delete(0, END)
  display_users()
  create_window.destroy()


# Function to read and display users
def display_users():
  for i in tree.get_children():
    tree.delete(i)
  cursor.execute("SELECT * FROM users")
  users = cursor.fetchall()
  for user in users:
    tree.insert('', 'end', values=user)


# Function to update a user
def update_user():
  selected_user = tree.item(tree.selection())['values']
  if not selected_user:
    return
  id = id_entry.get()
  name = name_entry.get()
  age = age_entry.get()
  cursor.execute("UPDATE users SET id = ?, name = ?, age = ? WHERE id = ?",
                 (id, name, age, selected_user[0]))
  conn.commit()
  id_entry.delete(0, END)
  name_entry.delete(0, END)
  age_entry.delete(0, END)
  display_users()
  update_window.destroy()


# Function to delete a user
def delete_user():
  selected_user = tree.item(tree.selection())['values']
  if not selected_user:
    return
  confirm = MessageBox.askyesno("Confirm",
                                "Are you sure you want to delete this user?")
  if confirm:
    cursor.execute("DELETE FROM users WHERE id=?", (selected_user[0], ))
    conn.commit()
  display_users()


#Function to check if any user is selected to be updated
def on_update_button_clicked():
  selected_user = tree.item(tree.selection())['values']
  if not selected_user:
    MessageBox.showerror("Error", "Please select a user to update.")
    return
  open_update_window()


#Function to check if any user is selected to delete
def on_delete_button_clicked():
  selected_user = tree.item(tree.selection())['values']
  if not selected_user:
    MessageBox.showerror("Error", "Please select a user to delete.")
    return
  delete_user()


# Function to open new window for Create
def open_create_window():
  global create_window
  create_window = Toplevel()
  create_window.title("Create")

  # ID label and entry
  id_label = Label(create_window, text="ID")
  id_label.grid(row=0, column=0, pady=10, padx=10)
  global id_entry
  id_entry = Entry(create_window)
  id_entry.grid(row=0, column=1, pady=10, padx=10)

  # Name label and entry
  name_label = Label(create_window, text="Name")
  name_label.grid(row=1, column=0, pady=10, padx=10)
  global name_entry
  name_entry = Entry(create_window)
  name_entry.grid(row=1, column=1, pady=10, padx=10)

  # Age label and entry
  age_label = Label(create_window, text="Age")
  age_label.grid(row=2, column=0, pady=10, padx=10)
  global age_entry
  age_entry = Entry(create_window)
  age_entry.grid(row=2, column=1, pady=10, padx=10)

  #Create button
  create_button = Button(create_window, text="Create", command=create_user)
  create_button.grid(row=3, column=2, pady=10, padx=10)


# Function to open new window for update
def open_update_window():
  global update_window
  update_window = Toplevel()
  update_window.title("Update")
  selected_user = tree.item(tree.selection())['values']

  # ID label and entry
  id_label = Label(update_window, text="ID")
  id_label.grid(row=0, column=0, pady=10, padx=10)
  global id_entry
  id_entry = Entry(update_window)
  id_entry.grid(row=0, column=1, pady=10, padx=10)
  id_entry.insert(0, selected_user[0])
  id_entry.config(state="readonly")

  # Name label and entry
  name_label = Label(update_window, text="Name")
  name_label.grid(row=1, column=0, pady=10, padx=10)
  global name_entry
  name_entry = Entry(update_window)
  name_entry.grid(row=1, column=1, pady=10, padx=10)
  name_entry.insert(0, selected_user[1])

  # Age label and entry
  age_label = Label(update_window, text="Age")
  age_label.grid(row=2, column=0, pady=10, padx=10)
  global age_entry
  age_entry = Entry(update_window)
  age_entry.grid(row=2, column=1, pady=10, padx=10)
  age_entry.insert(0, selected_user[2])

  #Update button
  update_button = Button(update_window, text="Update", command=update_user)
  update_button.grid(row=3, column=2, pady=10, padx=10)


#Treeview for users
tree = ttk.Treeview(root, columns=('id', 'name', 'age'), show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='Name')
tree.heading('age', text='Age')
tree.column('id', width=100, minwidth=50, anchor="center")
tree.column('name', width=200, minwidth=150, anchor="center")
tree.column('age', width=100, minwidth=50, anchor="center")
tree.pack(pady=20)

#Populate treeview with existing users
display_users()

#Create button
create_button = Button(root, text="Create", command=open_create_window)
create_button.pack(pady=10)

#Update button
update_button = Button(root, text="Update", command=on_update_button_clicked)
update_button.pack(pady=10)

#Delete button
delete_button = Button(root, text="Delete", command=on_delete_button_clicked)
delete_button.pack(pady=10)

root.mainloop()

#Close connection to database
conn.close()