import tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import sqlite3
from subprocess import call
import re

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title(" AI & Real Image Detection")
root.state("zoomed")
root.configure(bg="#eef1f7")

# ---------------- HEADER ----------------
header = tk.Frame(root, bg="#2f3e75", height=80)
header.pack(fill="x")

tk.Label(header,
         text="🧠AI & Real Image Detection",
         font=("Segoe UI", 26, "bold"),
         bg="#2f3e75",
         fg="white").pack(pady=20)

# ---------------- VARIABLES ----------------
username = tk.StringVar()
password = tk.StringVar()
attempts = 3

# ---------------- FUNCTIONS ----------------
def registration():
    call(["python", "Registration.py"])
    root.destroy()

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        show_btn.config(text="Hide")
    else:
        password_entry.config(show='*')
        show_btn.config(text="Show")

def open_forgot_password():
    root.destroy()
    call(["python", "forgot password.py"])

# ---------------- USERNAME VALIDATION ----------------
def validate_username():

    user = username.get().strip()

    if user == "":
        ms.showerror("Input Error", "Username cannot be empty")
        return False

    if len(user) < 3:
        ms.showerror("Input Error", "Username must be at least 3 characters")
        return False

    if not re.match("^[A-Za-z0-9@.]+$", user):
        ms.showerror("Input Error",
                     "Username can contain only letters, numbers, @ or .")
        return False

    return True

# ---------------- LOGIN FUNCTION ----------------
def login():
    global attempts

    if not validate_username():
        return

    if password.get() == "":
        ms.showerror("Input Error", "Password cannot be empty")
        return

    if attempts == 0:
        ms.showerror("Blocked", "Too many wrong attempts!\nLogin Disabled.")
        return

    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS admin_registration
                     (Fullname TEXT, address TEXT, username TEXT, Email TEXT,
                      Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)""")

        find_entry = 'SELECT * FROM admin_registration WHERE username=? AND password=?'
        c.execute(find_entry, (username.get(), password.get()))

        result = c.fetchall()

        if result:
            ms.showinfo("Success", "Login successful")
            root.destroy()
            call(["python", "GUI_Master_old.py"])

        else:
            attempts -= 1

            if attempts > 0:
                ms.showerror("Error",
                             f"Username or Password did not match.\nRemaining Attempts: {attempts}")
            else:
                ms.showerror("Blocked", "Too many wrong attempts!\nLogin Disabled.")
                login_btn.config(state="disabled")

# ---------------- CENTER CARD ----------------
card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.55, anchor="center", width=850, height=480)
card.config(highlightbackground="#d9d9d9", highlightthickness=1)

# ---------------- LEFT IMAGE SECTION ----------------
left_frame = tk.Frame(card, bg="#f4f6fb", width=400, height=480)
left_frame.pack(side="left", fill="both")

try:
    img = Image.open("secure.jpg")
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)

    img_label = tk.Label(left_frame, image=img, bg="#f4f6fb")
    img_label.image = img
    img_label.place(relx=0.5, rely=0.5, anchor="center")

except:
    tk.Label(left_frame,
             text="🔐",
             font=("Segoe UI", 120),
             bg="#f4f6fb",
             fg="#3f5bd9").place(relx=0.5, rely=0.5, anchor="center")

# ---------------- RIGHT LOGIN SECTION ----------------
right_frame = tk.Frame(card, bg="white", width=450, height=480)
right_frame.pack(side="right", fill="both", padx=40)

tk.Label(right_frame,
         text="Login to Your Account",
         font=("Segoe UI", 20, "bold"),
         bg="white",
         fg="#2f3e75").pack(pady=30)

# ---------------- USERNAME ----------------
tk.Label(right_frame,
         text="Username or Email Address",
         bg="white",
         font=("Segoe UI", 12)).pack(anchor="w")

user_frame = tk.Frame(right_frame, bg="white")
user_frame.pack(fill="x", pady=8)

username_entry = tk.Entry(user_frame,
                          textvariable=username,
                          font=("Segoe UI", 12))
username_entry.pack(fill="x")

# ---------------- PASSWORD ----------------
tk.Label(right_frame,
         text="Password",
         bg="white",
         font=("Segoe UI", 12)).pack(anchor="w")

pass_frame = tk.Frame(right_frame, bg="white")
pass_frame.pack(fill="x", pady=8)

password_entry = tk.Entry(pass_frame,
                          textvariable=password,
                          font=("Segoe UI", 12),
                          show="*")
password_entry.pack(side="left", fill="x", expand=True)

show_btn = tk.Button(pass_frame,
                     text="Show",
                     command=toggle_password,
                     bg="#3f5bd9",
                     fg="white",
                     bd=0,
                     font=("Segoe UI", 9, "bold"))
show_btn.pack(side="right", padx=5)

# ---------------- LOGIN BUTTON ----------------
login_btn = tk.Button(right_frame,
                      text="Login",
                      font=("Segoe UI", 14, "bold"),
                      command=login,
                      bg="#3f5bd9",
                      fg="white",
                      bd=0)
login_btn.pack(fill="x", pady=25)

# ---------------- REGISTER / FORGOT ----------------
bottom_frame = tk.Frame(right_frame, bg="white")
bottom_frame.pack()

tk.Label(bottom_frame,
         text="Don't have an account?",
         bg="white",
         font=("Segoe UI", 11)).pack(side="left")

tk.Button(bottom_frame,
          text="Signup",
          bg="white",
          fg="#3f5bd9",
          font=("Segoe UI", 11, "bold"),
          relief="flat",
          command=registration).pack(side="left", padx=5)

tk.Button(bottom_frame,
          text="Forgot Password?",
          font=("Segoe UI", 10, "bold"),
          command=open_forgot_password,
          bg="white",
          fg="#3f5bd9",
          bd=0).pack(side="left", padx=5)

root.mainloop()