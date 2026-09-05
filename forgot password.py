from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import smtplib
import random

root = Tk()
root.title("Change Password")
root.geometry("900x650")
root.configure(bg="#eef1f7")

# ---------------- HEADER ----------------
header = Frame(root, bg="#2f3e75", height=70)
header.pack(fill="x")

Label(header,
      text="🔐 Change Your Password",
      font=("Segoe UI",20,"bold"),
      bg="#2f3e75",
      fg="white").pack(pady=15)

# ---------------- VARIABLES ----------------
email = StringVar()
otp_var = StringVar()
new_password = StringVar()
confirm_password = StringVar()

generated_otp = ""
otp_time = 30
otp_verified = False

# ---------------- CARD ----------------
card = Frame(root,bg="white")
card.place(relx=0.5,rely=0.55,anchor="center",width=750,height=520)

# ---------------- LEFT IMAGE ----------------
left_frame = Frame(card,bg="#f4f6fb",width=300)
left_frame.pack(side="left",fill="both")

try:
    img = Image.open("secure.jpg")
    img = img.resize((250,250))
    img = ImageTk.PhotoImage(img)

    Label(left_frame,image=img,bg="#f4f6fb").place(relx=0.5,rely=0.5,anchor="center")

except:
    Label(left_frame,
          text="🔐",
          font=("Segoe UI",100),
          bg="#f4f6fb",
          fg="#3f5bd9").place(relx=0.5,rely=0.5,anchor="center")

# ---------------- RIGHT FRAME ----------------
right_frame = Frame(card,bg="white")
right_frame.pack(side="right",fill="both",expand=True,padx=40,pady=30)

Label(right_frame,
      text="Update Password",
      font=("Segoe UI",16,"bold"),
      bg="white",
      fg="#2f3e75").pack(anchor="w",pady=10)

form = Frame(right_frame,bg="white")
form.pack(pady=10)

# ---------------- ENTRY FUNCTION ----------------
def create_entry(label,var,row,show=None):

    Label(form,
          text=label,
          font=("Segoe UI",11),
          bg="white").grid(row=row,column=0,sticky="w",pady=8)

    Entry(form,
          textvariable=var,
          font=("Segoe UI",11),
          width=30,
          show=show).grid(row=row,column=1,pady=8,padx=10)

# ---------------- FORM FIELDS ----------------
create_entry("Email",email,0)
create_entry("Enter OTP",otp_var,1)
create_entry("New Password",new_password,2,show="*")
create_entry("Confirm Password",confirm_password,3,show="*")

# ---------------- TIMER LABEL ----------------
timer_label = Label(right_frame,
                    text="",
                    font=("Segoe UI",10),
                    bg="white",
                    fg="red")
timer_label.pack()

# ---------------- OTP TIMER ----------------
def countdown():

    global otp_time

    if otp_time > 0:
        timer_label.config(text=f"OTP expires in {otp_time} sec")
        otp_time -= 1
        root.after(1000,countdown)

    else:
        timer_label.config(text="OTP Expired ❌")

# ---------------- SEND OTP ----------------
def send_otp():

    global generated_otp
    global otp_time
    global otp_verified

    if email.get() == "":
        ms.showerror("Error","Enter Email First")
        return

    otp_verified = False
    generated_otp = str(random.randint(100000,999999))
    otp_time = 30

    try:

        sender_email = "ankitagadekar720@gmail.com"
        sender_password = "xozrrnyiycvdwbpw"

        message = f"Subject: Password Reset OTP\n\nYour OTP is {generated_otp}"

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,email.get(),message)
        server.quit()

        ms.showinfo("OTP Sent","OTP sent to your email")

        countdown()

    except:
        ms.showerror("Error","Unable to send OTP")

# ---------------- VERIFY OTP ----------------
def verify_otp():

    global otp_verified
    global generated_otp

    # NEW CHECK ADDED
    if generated_otp == "":
        ms.showerror("Error","Please click 'Send OTP' first")
        return

    if otp_var.get() == "":
        ms.showerror("Error","Please enter OTP")
        return

    if otp_time == 0:
        ms.showerror("Error","OTP Expired")
        return

    if otp_var.get() == generated_otp:

        otp_verified = True
        generated_otp = ""   # Prevent OTP reuse
        ms.showinfo("Success","OTP Verified Successfully")

    else:
        ms.showerror("Error","Invalid OTP")

# ---------------- CHANGE PASSWORD ----------------
def change_password():

    if email.get()=="" or new_password.get()=="" or confirm_password.get()=="":

        ms.showerror("Error","All fields required")
        return

    if not otp_verified:

        ms.showerror("Error","Please verify OTP first")
        return

    if new_password.get()!=confirm_password.get():

        ms.showerror("Error","Passwords do not match")
        return

    with sqlite3.connect('evaluation.db') as db:

        c = db.cursor()

        c.execute("SELECT * FROM admin_registration WHERE Email=?",
                  (email.get(),))

        result = c.fetchone()

        if result:

            c.execute("UPDATE admin_registration SET password=? WHERE Email=?",
                      (new_password.get(),email.get()))

            db.commit()

            ms.showinfo("Success","Password Updated Successfully")
            root.destroy()

        else:

            ms.showerror("Error","Invalid Email")

# ---------------- BUTTONS ----------------
Button(right_frame,
       text="Send OTP",
       font=("Segoe UI",11,"bold"),
       bg="#3f5bd9",
       fg="white",
       width=15,
       bd=0,
       command=send_otp).pack(pady=5)

Button(right_frame,
       text="Verify OTP",
       font=("Segoe UI",11,"bold"),
       bg="#28a745",
       fg="white",
       width=15,
       bd=0,
       command=verify_otp).pack(pady=5)

Button(right_frame,
       text="Update Password",
       font=("Segoe UI",12,"bold"),
       bg="#ff9800",
       fg="white",
       width=20,
       bd=0,
       command=change_password).pack(pady=20)

root.mainloop()