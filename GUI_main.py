import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from subprocess import call

# ---------------- Main Window ----------------
root = tk.Tk()
root.title("AI & Real Image Detection")

# Fullscreen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.resizable(False, False)
root.configure(bg="#eef1f7")

# ---------------- Header ----------------
header = tk.Frame(root, bg="#2f3e75", height=80)
header.pack(fill="x")

title_label = tk.Label(
    header,
    text="🧠 AI & Real Image Detection",
    font=('Segoe UI', 26, 'bold'),
    bg="#2f3e75",
    fg="white"
)
title_label.pack(pady=20)

# ---------------- Center Card ----------------
card = tk.Frame(root, bg="white", bd=0)
card.place(relx=0.5, rely=0.5, anchor="center", width=550, height=450)
card.config(highlightbackground="#d9d9d9", highlightthickness=1)

# ---------------- Shield Icon ----------------
try:
    icon_img = Image.open("secure.jpg").resize((140, 140), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon_img)
    icon_label = tk.Label(card, image=icon, bg="white")
    icon_label.image = icon
    icon_label.pack(pady=15)
except:
    icon_label = tk.Label(card, text="🔐", font=('Segoe UI', 60), bg="white")
    icon_label.pack(pady=15)

# ---------------- Welcome Text ----------------
welcome_label = tk.Label(
    card,
    text="Welcome to AI & Real Image Detection System",
    font=('Segoe UI', 13),
    bg="white",
    fg="#555555"
)
welcome_label.pack(pady=5)

# ---------------- Button Functions ----------------
def open_login():
    call(["python", "Login.py"])

def open_register():
    call(["python", "Registration.py"])

def exit_app():
    root.destroy()

# ---------------- Button Style ----------------
button_style = {
    "font": ('Segoe UI', 14, 'bold'),
    "bg": "#3f5bd9",
    "fg": "white",
    "activebackground": "#3249b5",
    "activeforeground": "white",
    "bd": 0,
    "width": 18,
    "height": 2,
    "cursor": "hand2"
}

# Hover effect
def on_enter(e):
    e.widget.config(bg="#3249b5")

def on_leave(e):
    e.widget.config(bg="#3f5bd9")

# ---------------- Buttons ----------------
btn_login = tk.Button(card, text="Login", command=open_login, **button_style)
btn_login.pack(pady=15)
btn_login.bind("<Enter>", on_enter)
btn_login.bind("<Leave>", on_leave)

btn_register = tk.Button(card, text="Register", command=open_register, **button_style)
btn_register.pack(pady=10)
btn_register.bind("<Enter>", on_enter)
btn_register.bind("<Leave>", on_leave)

btn_exit = tk.Button(
    card,
    text="Exit",
    command=exit_app,
    font=('Segoe UI', 12),
    bg="white",
    fg="#3f5bd9",
    bd=0,
    cursor="hand2"
)
btn_exit.pack(pady=10)



root.mainloop()