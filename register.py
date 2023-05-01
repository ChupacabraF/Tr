import tkinter

import customtkinter as ctk
import requests
import re


class Register(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ctk.set_default_color_theme("green")

        title_label = ctk.CTkLabel(self, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        vcmd = (self.register(self.validate), '%P')
        self.loginname_entry = ctk.CTkEntry(self, placeholder_text="Loginname", width=400, height=50)
        self.loginname_entry.configure(validate='key', validatecommand=vcmd)
        self.loginname_entry.pack(pady=8, padx=20)

        self.label_error = ctk.CTkLabel(self)
        self.label_error.pack(pady=8, padx=20)

        password_entry = ctk.CTkEntry(self, placeholder_text="Passwort", width=400, height=50)
        password_entry.pack(pady=8, padx=20)

        vorname_entry = ctk.CTkEntry(self, placeholder_text="Vorname", width=400, height=50)
        vorname_entry.pack(pady=8, padx=20)

        nachname_entry = ctk.CTkEntry(self, placeholder_text="Nachname", width=400, height=50)
        nachname_entry.pack(pady=8, padx=20)

        strasse_entry = ctk.CTkEntry(self, placeholder_text="Straße", width=400, height=50)
        strasse_entry.pack(pady=8, padx=20)

        search_ort = (self.register(self.abfrage_ort_zu_plz), '%P')
        self.plz_entry = ctk.CTkEntry(self, placeholder_text="PLZ", width=400, height=50)
        self.plz_entry.configure(validate='focusout', validatecommand=search_ort)
        self.plz_entry.pack(pady=8, padx=20)

        # Soll automatisch gesetzt werden
        self.ort_entry = ctk.CTkEntry(self, placeholder_text="Ort", width=400, height=50, state=tkinter.NORMAL)
        self.ort_entry.pack(pady=8, padx=20)

        land_entry = ctk.CTkEntry(self, placeholder_text="Land", width=400, height=50)
        land_entry.pack(pady=8, padx=20)

        telefon_entry = ctk.CTkEntry(self, placeholder_text="Telefon", width=400, height=50)
        telefon_entry.pack(pady=8, padx=20)

        email_adresse_entry = ctk.CTkEntry(self, placeholder_text="E-Mail Adresse", width=400, height=50)
        email_adresse_entry.pack(pady=8, padx=20)

        register_button = ctk.CTkButton(self, text="Register", width=300, height=35,
                                        command=lambda: self.register_user(self.loginname_entry.get(),
                                                                           password_entry.get(),
                                                                           vorname_entry.get(),
                                                                           nachname_entry.get(),
                                                                           strasse_entry.get(), self.plz_entry.get(),
                                                                           land_entry.get(), telefon_entry.get(),
                                                                           email_adresse_entry.get()))
        register_button.pack(pady=16, padx=20)

        already_registered_label = ctk.CTkLabel(self, text="Already registered? Than go to login!",
                                                font=ctk.CTkFont(size=14, weight="normal"))
        already_registered_label.pack(padx=10, pady=(20, 0))

        login_button = ctk.CTkButton(self, text="Login", width=300, height=35, command=login)
        login_button.pack(pady=5, padx=20)

    def show_message(self, error='', color='black'):
        self.label_error['text'] = error
        self.loginname_entry['foreground'] = color

    # TODO cmn das kann gut für Mail genutzt werden
    def validate(self, value):
        """
        Validat the email entry
        :param self:
        :param value:
        :return:
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value) is None:
            return False

        self.show_message()
        return True

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        self.show_message('Please enter a valid email', 'red')

    # Muss ausgeführt werden, sobald die PLZ eingegeben wird
    def abfrage_ort_zu_plz(self, plz):
        # Wann muss diese benutzt werden?
        # http://api.geonames.org/postalCodeSearchJSON?postalcode=46397&username=isjupr

        # URL des Endpunkts
        url = "http://api.geonames.org/postalCodeSearchJSON"

        # Query-Parameter
        params = {
            "postalcode": plz,
            "username": "demo"
        }

        # GET-Anfrage senden
        response = requests.get(url, params=params)

        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt:")
            print(response.json())

            self.ort_entry.insert(0, response.json()["postalCodes"][0]["placeName"])
            return True
        else:
            print("Fehler bei der Anfrage. Statuscode:", response.status_code)
            return True

    def nutzername_pruefen(self, nutzername):
        if nutzername != 'Username' and nutzername is not None and nutzername != '':
            # URL des Endpunkts
            url = "https://fapfa.azurewebsites.net/FAPServer/service/fapservice/checkLoginName"

            # Query-Parameter
            params = {"id": nutzername}

            # GET-Anfrage senden
            response = requests.get(url, params=params)

            # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
            if response.status_code == 200:
                # Antwortinhalt als Text ausgeben
                print("Antwortinhalt:", response.text)
                return True
            else:
                print("Fehler bei der Anfrage. Statuscode:", response.status_code)
                return False

    def register_user(self, login_name, passwort, vorname, nachname, strasse, plz, land, telefon, email_adresse):
        # register webservice call
        print("Registering")

        # Prüfung des Benutzernamens auf Eindeutigkeit
        if self.nutzername_pruefen(login_name):
            print("Nutzername noch nicht vorhanden")
            # Abfrage des Orts zur PLZ - GET
            ort = self.abfrage_ort_zu_plz(plz)

            # Registierung des neuen Benutzers
            # URL des Endpunkts
            url = 'https://fapfa.azurewebsites.net/FAPServer/service/fapservice/addUser'

            # Daten, die an den Endpunkt gesendet werden sollen (als JSON)
            data = {
                'loginName': login_name,
                'passwort': passwort,
                'passwort': passwort,
                'vorname': vorname,
                'nachname': nachname,
                'strasse': strasse,
                'plz': plz,
                'ort': ort,
                'land': land,
                'telefon': telefon,
                'email': email_adresse
            }

            # Senden des POST-Requests
            response = requests.post(url, json=data)

            # Überprüfen der Response
            if response.status_code == 200:
                print('Benutzer wurde erfolgreich hinzugefügt.')
            else:
                print('Fehler beim Hinzufügen des Benutzers. Statuscode:', response.status_code)
        else:
            print("Nutzername schon vorhanden")


def login():
    # go to login view
    print("logging in")
    # view_login = login_view()
    # login_view().mainloop()
