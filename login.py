import customtkinter as ctk
import requests
from register import Register


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

        login_button = ctk.CTkButton(self, text="Login", width=300, height=35, command=lambda: login(self.loginname_entry, password_entry.get()))
        login_button.pack(pady=16, padx=20)

        self.current_view = Register(master=self)
        register_button = ctk.CTkButton(self, text="Register", width=200, height=35,
                                        command=lambda: master.switch_frame(Register))
        register_button.pack(pady=100, padx=20)


def login(login_name, passwort):
    if((login_name != '') & (passwort != '')):
        abfrage_login(login_name, passwort)
    else:
        #############TODO#########################################
        #Message an User, dass Eingabefelder befüllt werden müssen
        print('Gebe die Logindaten ein')
        ##########################################################

    

def abfrage_login(login_name, passwort):

    url = 'https://fapfa.azurewebsites.net/FAPServer/service/fapservice/login'

    # Daten, die an den Endpunkt gesendet werden sollen (als JSON)
    data = {
        'loginName': login_name,
        'passwort': passwort,
    }

    # Senden des POST-Requests
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print('Benutzer wurde erfolgreich eingeloggt.')
        session = response.body
    else:
        print('Fehler beim Login des Benutzers. Statuscode:', response.status_code)
        #############TODO########################################
        #Message an User, dass Username oder Passwort falsch sind
        #########################################################