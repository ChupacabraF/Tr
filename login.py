import customtkinter as ctk
import requests
from register import Register
from CTkMessagebox import CTkMessagebox


# let the fun begin!
class Login(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        title_label = ctk.CTkLabel(self, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        self.loginname_entry = ctk.CTkEntry(self, placeholder_text="Loginname", width=400, height=50)
        self.loginname_entry.pack(pady=8, padx=20)

        password_entry = ctk.CTkEntry(self, placeholder_text="Password", width=400, height=50)
        password_entry.pack(pady=8, padx=20, )

        login_button = ctk.CTkButton(self, text="Login", width=300, height=35, command=lambda: login(self.loginname_entry.get(), password_entry.get(), master))
        login_button.pack(pady=16, padx=20)

        self.current_view = Register(master=self)
        register_button = ctk.CTkButton(self, text="Register", width=200, height=35,
                                        command=lambda: master.switch_frame(Register))
        register_button.pack(pady=100, padx=20)


def login(login_name, passwort, master):
    if((login_name != '') & (passwort != '')):
        abfrage_login(login_name, passwort, master)
    else:
        #############TODO#########################################
        #Message an User, dass Eingabefelder befüllt werden müssen
        show_info("", "Gib deine vollständigen Logindaten ein.")
        ##########################################################

    

def abfrage_login(login_name, passwort, master):

    url = 'https://fapfa.azurewebsites.net/FAPServer/service/fapservice/login'

    # Daten, die an den Endpunkt gesendet werden sollen (als JSON)
    data = {
        "loginName": login_name,
        "passwort": {'passwort': passwort},
    }

    # Senden des POST-Requests
    response = requests.post(url, json=data)
    responseObj = response.json()
    try:
        if responseObj.sessionID != "":
            print('Benutzer wurde erfolgreich eingeloggt.')
            session = response.content
            master.switch_frame(Register)
    except:
        show_warning("Fehler beim Login", "Der Loginname oder das Kennwort sind falsch.")
        
    


def show_info(title, message):
    # Default messagebox for showing some information
    CTkMessagebox(title=title, message=message)

def show_warning(title, warning):
    # Show some retry/cancel warnings
    msg = CTkMessagebox(title=title, message=warning,
                  icon="warning", option_1="Ok")
