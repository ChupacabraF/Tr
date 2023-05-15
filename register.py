import tkinter
import customtkinter as ctk
import requests
import re

import settings


# from fapUebersicht import FapUebersicht


class Register(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ctk.set_default_color_theme("green")
        title_label = ctk.CTkLabel(self, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        # Loginname Feld mit Validierung und Label
        loginname_validieren = (self.register(self.validate_loginname), '%P')
        self.loginname_entry = ctk.CTkEntry(self, placeholder_text="Loginname", width=400, height=50)
        self.loginname_entry.configure(validate='focusout', validatecommand=loginname_validieren)
        self.loginname_entry.pack(pady=8, padx=20)
        self.loginname_label_error = ctk.CTkLabel(self, text='Loginname bereits vergeben', text_color='red')

        # Passwort Feld
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Passwort", width=400, height=50)
        self.password_entry.pack(pady=8, padx=20)

        # Passwort-Wiederholen Feld
        password_wiederholen_validieren = (self.register(self.validate_password_wiederholen), '%P')
        self.password_wiederholen_entry = ctk.CTkEntry(self, placeholder_text="Passwort wiederholen", width=400,
                                                       height=50)
        self.password_wiederholen_entry.configure(validate='focusout', validatecommand=password_wiederholen_validieren)
        self.password_wiederholen_entry.pack(pady=8, padx=20)
        self.password_wiederholen_label_error = ctk.CTkLabel(self, text='Passwort unterschiedlich', text_color='red')

        # Vorname Feld
        vorname_entry = ctk.CTkEntry(self, placeholder_text="Vorname", width=400, height=50)
        vorname_entry.pack(pady=8, padx=20)

        # Nachname Feld
        nachname_entry = ctk.CTkEntry(self, placeholder_text="Nachname", width=400, height=50)
        nachname_entry.pack(pady=8, padx=20)

        # Telefonnummer Feld
        telefon_entry = ctk.CTkEntry(self, placeholder_text="Telefon", width=400, height=50)
        telefon_entry.pack(pady=8, padx=20)

        # E-Mail-Feld mit Validierung
        email_adresse_validieren = (self.register(self.validate_mail_adresse), '%P')
        self.email_adresse_entry = ctk.CTkEntry(self, placeholder_text="E-Mail Adresse", width=400, height=50)
        self.email_adresse_entry.configure(validate='focusout', validatecommand=email_adresse_validieren)
        self.email_adresse_entry.pack(pady=8, padx=20)
        self.email_adresse_label_error = ctk.CTkLabel(self, text='E-Mail Adresse nicht gültig', text_color='red')

        # Straße Feld
        strasse_entry = ctk.CTkEntry(self, placeholder_text="Straße", width=400, height=50)
        strasse_entry.pack(pady=8, padx=20)

        # PLZ Feld
        search_ort = (self.register(self.abfrage_ort_zu_plz), '%P')
        self.plz_entry = ctk.CTkEntry(self, placeholder_text="PLZ", width=400, height=50)
        self.plz_entry.configure(validate='focusout', validatecommand=search_ort)
        self.plz_entry.pack(pady=8, padx=20)

        # Ort Feld wirt automatisch anhand der PLZ gesetzt
        self.ort_entry = ctk.CTkEntry(self, placeholder_text="Ort", width=400, height=50, state=tkinter.NORMAL)
        self.ort_entry.pack(pady=8, padx=20)

        # Land Feld
        land_entry = ctk.CTkEntry(self, placeholder_text="Land", width=400, height=50)
        land_entry.pack(pady=8, padx=20)

        # Registrierungsbutton
        register_button = ctk.CTkButton(self, text="Register", width=300, height=35,
                                        command=lambda: self.register_user(master, self.loginname_entry.get(),
                                                                           self.password_entry.get(),
                                                                           vorname_entry.get(),
                                                                           nachname_entry.get(),
                                                                           strasse_entry.get(), self.plz_entry.get(),
                                                                           land_entry.get(), telefon_entry.get(),
                                                                           self.email_adresse_entry.get()))
        register_button.pack(pady=16, padx=20)

        # Schon registriert?
        already_registered_label = ctk.CTkLabel(self, text="Already registered? Than go to login!",
                                                font=ctk.CTkFont(size=14, weight="normal"))
        already_registered_label.pack(padx=10, pady=(20, 0))
        login_button = ctk.CTkButton(self, text="Login", width=300, height=35, command=login)
        login_button.pack(pady=5, padx=20)

    def validate_mail_adresse(self, mailadresse):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        matched = bool(re.match(pattern, mailadresse))
        if matched:
            self.email_adresse_label_error.pack_forget()
            return True
        else:
            self.email_adresse_label_error.pack(pady=8, padx=20, after=self.email_adresse_entry)
            return False

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
            return response.json()["postalCodes"][0]["placeName"]
        else:
            print("Fehler bei der Anfrage. Statuscode:", response.status_code)
            return False

    def validate_loginname(self, nutzername):
        if nutzername != 'Username' and nutzername is not None and nutzername != '':
            # URL des Endpunkts
            url = f'{settings.baseUri}/checkLoginName'

            # Query-Parameter
            params = {"id": nutzername}

            # GET-Anfrage senden
            response = requests.get(url, params=params)

            # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
            if response.status_code == 200:
                if response.json()["ergebnis"]:
                    # Antwortinhalt als Text ausgeben
                    print("Antwortinhalt:", response.text)
                    self.loginname_label_error.pack_forget()
                    return True
                else:
                    print("Fehler bei der Anfrage. Statuscode:", response.status_code)
                    self.loginname_label_error.pack(pady=8, padx=20, after=self.loginname_entry)
                    return False

    def validate_password_wiederholen(self, password):
        if password != self.password_entry.get():
            self.password_wiederholen_label_error.pack(pady=8, padx=20, after=self.password_wiederholen_entry)
            return False
        else:
            self.password_wiederholen_label_error.pack_forget()
            return True

    def register_user(self, master, login_name, passwort, vorname, nachname, strasse, plz, land, telefon,
                      email_adresse):
        # register webservice call
        print("Registering")

        # Prüfung des Benutzernamens auf Eindeutigkeit
        if self.validate_loginname(login_name):
            print("Nutzername noch nicht vorhanden")
            # Abfrage des Orts zur PLZ - GET
            ort = self.abfrage_ort_zu_plz(plz)

            # Registierung des neuen Benutzers
            # URL des Endpunkts
            url = f'{settings.baseUri}/addUser'

            # Daten, die an den Endpunkt gesendet werden sollen (als JSON)
            data = {
                "loginName": login_name,
                "passwort": {'passwort': passwort},
                "vorname": vorname,
                "nachname": nachname,
                "strasse": strasse,
                "plz": plz,
                "ort": ort,
                "land": land,
                "telefon": telefon,
                "email": email_adresse
            }

            # Senden des POST-Requests
            response = requests.post(url, json=data)

            # Überprüfen der Response
            if response.status_code == 200:
                if response.json()["ergebnis"]:
                    print('Benutzer wurde erfolgreich registriert.')
                    # master.switch_frame((FapUebersicht(master, login_name, response.json()['sessionID'])))
                else:
                    print('Fehler beim Hinzufügen des Benutzers. Statuscode:', response.status_code)
        else:
            print("Nutzername schon vorhanden")


def login():
    # go to login view
    print("logging in")
    # view_login = login_view()
    # login_view().mainloop()
