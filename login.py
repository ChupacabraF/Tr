import customtkinter as ctk
from PIL import Image
from register import Register


# let the fun begin!
class Login(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # title_image = ctk.CTkImage(Image.open("TrackMate Logo.png"), size=(50, 50))

        title_label = ctk.CTkLabel(self, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=400, height=50)
        username_entry.pack(pady=8, padx=20)

        password_entry = ctk.CTkEntry(self, placeholder_text="Password", width=400, height=50)
        password_entry.pack(pady=8, padx=20, )

        # login_button = ctk.CTkButton(self, text="Login", width=300, height=35, command=login)
        # login_button.pack(pady=16, padx=20)

        self.current_view = Register(master=self)
        register_button = ctk.CTkButton(self, text="Register", width=200, height=35,
                                        command=lambda: master.switch_frame(Register))
        register_button.pack(pady=100, padx=20)