import customtkinter as ctk
from PIL import Image

#let the fun begin!

def login():      

    # login call
    print("logging in")

def register():      

    # register call
    print("registering")


ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("960x540")
root.title("TrackMate")

#title_image = ctk.CTkImage(Image.open("TrackMate Logo.png"), size=(50, 50))

title_label = ctk.CTkLabel(root, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(padx=10, pady=(40, 20))

username_entry = ctk.CTkEntry(root, placeholder_text="Username", width=400, height=50)
username_entry.pack(pady=8, padx=20)

password_entry = ctk.CTkEntry(root, placeholder_text="Password", width=400, height=50)
password_entry.pack(pady=8, padx=20,)

login_button = ctk.CTkButton(root, text="Login", width=300, height=35, command=login)
login_button.pack(pady=16, padx=20)

login_button = ctk.CTkButton(root, text="Register", width=200, height=35, command=register)
login_button.pack(pady=100, padx=20)

root.mainloop()