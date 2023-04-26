import customtkinter as ctk
from PIL import Image
import requests


class Register(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ctk.set_default_color_theme("green")

        title_label = ctk.CTkLabel(self, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        loginname_entry = ctk.CTkEntry(self, placeholder_text="Loginname", width=400, height=50)
        loginname_entry.pack(pady=8, padx=20)

        password_entry = ctk.CTkEntry(self, placeholder_text="Passwort", width=400, height=50)
        password_entry.pack(pady=8, padx=20, )

        vorname_entry = ctk.CTkEntry(self, placeholder_text="Vorname", width=400, height=50)
        vorname_entry.pack(pady=8, padx=20, )

        nachname_entry = ctk.CTkEntry(self, placeholder_text="Nachname", width=400, height=50)
        nachname_entry.pack(pady=8, padx=20, )

        strasse_entry = ctk.CTkEntry(self, placeholder_text="Straße", width=400, height=50)
        strasse_entry.pack(pady=8, padx=20, )

        plz_entry = ctk.CTkEntry(self, placeholder_text="PLZ", width=400, height=50)
        plz_entry.pack(pady=8, padx=20, )

        land_entry = ctk.CTkEntry(self, placeholder_text="Land", width=400, height=50)
        land_entry.pack(pady=8, padx=20, )

        telefon_entry = ctk.CTkEntry(self, placeholder_text="Telefon", width=400, height=50)
        telefon_entry.pack(pady=8, padx=20, )

        email_adresse_entry = ctk.CTkEntry(self, placeholder_text="E-Mail Adresse", width=400, height=50)
        email_adresse_entry.pack(pady=8, padx=20, )

        register_button = ctk.CTkButton(self, text="Register", width=300, height=35,
                                        command=lambda: register(loginname_entry.get(), password_entry.get(),
                                                                 vorname_entry.get(),
                                                                 nachname_entry.get(),
                                                                 strasse_entry.get(), plz_entry.get(),
                                                                 land_entry.get(), telefon_entry.get(),
                                                                 email_adresse_entry.get()))
        register_button.pack(pady=16, padx=20)

        already_registered_label = ctk.CTkLabel(self, text="Already registered? Than go to login!",
                                                font=ctk.CTkFont(size=14, weight="normal"))
        already_registered_label.pack(padx=10, pady=(20, 0))

        login_button = ctk.CTkButton(self, text="Login", width=300, height=35, command=login)
        login_button.pack(pady=5, padx=20)


def nutzername_pruefen(nutzername):
    # URL des Endpunkts
    url = "http://localhost:8080/FAPServer/service/fapservice/checkLoginName"

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


def abfrage_ort_zu_plz(plz):
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
        return response.json()["postalCodes"][0]["placeName"]
    else:
        print("Fehler bei der Anfrage. Statuscode:", response.status_code)
        return ""


def register(login_name, passwort, vorname, nachname, strasse, plz, land, telefon, email_adresse):
    # register webservice call
    print("Registering")

    # Hier erstmal Prüfung des Benutzernamens auf Eindeutigkeit
    if nutzername_pruefen(login_name):
        print("Nutzername noch nicht vorhanden")
    else:
        print("Nutzername schon vorhanden")

    # Abfrage des Orts zur PLZ - GET
    ort = abfrage_ort_zu_plz(plz)

    # Registierung des neuen Benutzers
    # URL des Endpunkts
    url = 'http://localhost:8080/FAPServer/service/fapservice/addUser'

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


def login():
    # go to login view
    print("logging in")
    # view_login = login_view()
    # login_view().mainloop()
