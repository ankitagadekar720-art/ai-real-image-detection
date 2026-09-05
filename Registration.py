import tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import sqlite3
from subprocess import call
import random
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.configure(bg='#eef1f7')
root.geometry("1000x600")
root.title("Registration Form")

# ---------------- HEADER ----------------
header = tk.Frame(root, bg="#2f3e75", height=60)
header.pack(fill="x")

tk.Label(header, text="🧠 AI & Real Image Detection",
         font=("Segoe UI", 20, "bold"),
         bg="#2f3e75", fg="white").pack(pady=12)

# ---------------- VARIABLES ----------------
Fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
Email = tk.StringVar()
Phoneno = tk.StringVar()
Gender = tk.StringVar()
age = tk.StringVar()
password = tk.StringVar()
confirm_password = tk.StringVar()
otp_var = tk.StringVar()

generated_otp = ""
otp_timer = 0
otp_verified = False

# ---------------- DATABASE ----------------
with sqlite3.connect('evaluation.db') as db:
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS admin_registration(
                 Fullname TEXT, address TEXT, username TEXT, Email TEXT,
                 Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)""")
    db.commit()

# ---------------- USERNAME VALIDATION ----------------
def validate_username():

    user = username.get()

    if not re.match("^[A-Za-z0-9]+$", user):
        ms.showerror("Error", "Username should contain only letters and numbers")
        return False

    if len(user) < 3:
        ms.showerror("Error", "Username must be at least 3 characters")
        return False

    return True


# ---------------- PHONE VALIDATION ----------------
def validate_phone(P):

    if P.isdigit() or P == "":
        return True
    else:
        return False


# ---------------- PASSWORD VALIDATION ----------------
def password_check(passwd):

    if len(passwd) < 8:
        return False
    if not re.search("[A-Z]", passwd):
        return False
    if not re.search("[a-z]", passwd):
        return False
    if not re.search("[0-9]", passwd):
        return False
    if not re.search("[@#$%^&+=!]", passwd):
        return False

    return True


# ---------------- OTP TIMER ----------------
def countdown():

    global otp_timer

    if otp_timer > 0:
        timer_label.config(text=f"OTP expires in {otp_timer} sec")
        otp_timer -= 1
        root.after(1000, countdown)
    else:
        timer_label.config(text="OTP Expired")


# ---------------- SEND OTP ----------------
def send_otp():

    global generated_otp, otp_timer, otp_verified

    if not re.match(r"[^@]+@[^@]+\.[^@]+", Email.get()):
        ms.showerror("Error", "Enter valid Email first!")
        return

    generated_otp = str(random.randint(1000, 9999))
    otp_verified = False

    try:

        sender_email = "ankitagadekar720@gmail.com"
        sender_password = "xozrrnyiycvdwbpw"

        receiver_email = Email.get()

        message = MIMEMultipart("alternative")
        message["Subject"] = "OTP for Registration"
        message["From"] = sender_email
        message["To"] = receiver_email

        body = f"""
Hello,

Your OTP is: {generated_otp}

It will expire in 30 seconds.

Thank You.
"""

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        otp_timer = 30
        countdown()

        ms.showinfo("Success", "OTP sent to your Email!")

    except Exception as e:

        ms.showerror("Error", f"Failed to send OTP\n{e}")


# ---------------- VERIFY OTP ----------------
def verify_otp():

    global otp_verified

    if otp_timer == 0:
        ms.showerror("Error", "OTP Expired! Please resend OTP")
        return

    if otp_var.get() == "":
        ms.showerror("Error", "Enter OTP")
        return

    if otp_var.get() == generated_otp:

        otp_verified = True
        ms.showinfo("Success", "OTP Verified Successfully!")

    else:

        ms.showerror("Error", "Incorrect OTP")


# ---------------- REGISTER FUNCTION ----------------
def register():

    if (not Fullname.get() or not address.get() or not username.get() or not Email.get()
            or not Phoneno.get() or not Gender.get() or not age.get()
            or not password.get() or not confirm_password.get()):
        ms.showerror("Error", "All fields are required!")
        return

    if not validate_username():
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", Email.get()):
        ms.showerror("Error", "Invalid Email format")
        return

    if len(Phoneno.get()) != 10:
        ms.showerror("Error", "Phone number must be 10 digits")
        return

    if not age.get().isdigit() or int(age.get()) < 18:
        ms.showerror("Error", "Age must be 18 or above")
        return

    if not password_check(password.get()):
        ms.showerror("Error",
                     "Password must contain:\n"
                     "• 8 characters\n"
                     "• 1 Uppercase\n"
                     "• 1 Lowercase\n"
                     "• 1 Number\n"
                     "• 1 Special character")
        return

    if password.get() != confirm_password.get():
        ms.showerror("Error", "Passwords do not match")
        return

    if not otp_verified:
        ms.showerror("Error", "Please verify OTP first")
        return

    with sqlite3.connect('evaluation.db') as db:

        c = db.cursor()

        c.execute("INSERT INTO admin_registration VALUES (?,?,?,?,?,?,?,?)",
                  (Fullname.get(), address.get(), username.get(),
                   Email.get(), Phoneno.get(), Gender.get(),
                   age.get(), password.get()))

        db.commit()

    ms.showinfo("Success", "Account Created Successfully!")

    root.destroy()
    call(["python", "Login.py"])


# ---------------- BACK ----------------
def go_back():
    root.destroy()
    call(["python", "GUI_main.py"])


# ---------------- CENTER CARD ----------------
card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.55, anchor="center", width=980, height=480)

left_frame = tk.Frame(card, bg="#f4f6fb", width=400, height=480)
left_frame.pack(side="left", fill="both")

try:

    img = Image.open("secure.jpg")
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)

    tk.Label(left_frame, image=img, bg="#f4f6fb").place(relx=0.5, rely=0.5, anchor="center")

except:

    tk.Label(left_frame,
             text="🔐",
             font=("Segoe UI", 120),
             bg="#f4f6fb",
             fg="#3f5bd9").place(relx=0.5, rely=0.5, anchor="center")

right_frame = tk.Frame(card, bg="white")
right_frame.pack(fill="both", expand=True, padx=40, pady=20)

tk.Label(right_frame, text="Registration Form",
         font=("Segoe UI", 18, "bold"),
         bg="white", fg="#2f3e75").pack(anchor="w")

form = tk.Frame(right_frame, bg="white")
form.pack(pady=10)

# phone validation
vcmd = (root.register(validate_phone), '%P')


def create_entry(label, var, row, show=None, validate=None):

    tk.Label(form, text=label, bg="white",
             font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", pady=5)

    entry = tk.Entry(form,
                     textvariable=var,
                     font=("Segoe UI", 10),
                     width=30,
                     show=show)

    if validate:
        entry.config(validate="key", validatecommand=vcmd)

    entry.grid(row=row, column=1, pady=5, padx=8)

    return entry


create_entry("Full Name", Fullname, 0)
create_entry("Address", address, 1)
create_entry("Username", username, 2)
create_entry("Email", Email, 3)

tk.Button(form,
          text="Send OTP",
          command=send_otp,
          bg="#3f5bd9",
          fg="white",
          font=("Segoe UI", 8, "bold"),
          bd=0).grid(row=3, column=2, padx=5)

create_entry("Phone No.", Phoneno, 4, validate=True)
create_entry("Age", age, 5)

tk.Label(form, text="Gender", bg="white",
         font=("Segoe UI", 10)).grid(row=6, column=0, sticky="w")

gender_frame = tk.Frame(form, bg="white")
gender_frame.grid(row=6, column=1, pady=5)

tk.Radiobutton(gender_frame, text="Male",
               variable=Gender, value="Male", bg="white").pack(side="left", padx=5)

tk.Radiobutton(gender_frame, text="Female",
               variable=Gender, value="Female", bg="white").pack(side="left", padx=5)

tk.Radiobutton(gender_frame, text="Other",
               variable=Gender, value="Other", bg="white").pack(side="left", padx=5)

create_entry("Password", password, 7, show="*")
create_entry("Confirm Password", confirm_password, 8, show="*")
create_entry("Enter OTP", otp_var, 9)

tk.Button(form,
          text="Verify OTP",
          command=verify_otp,
          bg="#28a745",
          fg="white",
          font=("Segoe UI", 8, "bold"),
          bd=0).grid(row=9, column=2)

timer_label = tk.Label(form, text="", bg="white",
                       fg="red", font=("Segoe UI", 9))
timer_label.grid(row=9, column=3)

# ---------------- BUTTONS ----------------
btn_frame = tk.Frame(right_frame, bg="white")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Register",
          font=("Segoe UI", 12, "bold"),
          command=register,
          bg="#3f5bd9", fg="white",
          width=18, bd=0).pack(side="left", padx=10)

tk.Button(btn_frame, text="Back",
          font=("Segoe UI", 12, "bold"),
          command=go_back,
          bg="#aaaaaa", fg="white",
          width=10, bd=0).pack(side="left", padx=10)

root.mainloop()