import json
import threading
import tkinter
import re
import customtkinter as ctk
import requests
from CTkMessagebox import CTkMessagebox
import tkintermapview as mapView
import settings


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Hauptfenster der Anwendung konfigurieren
        self.title("TrackMate")
        self.geometry("800x600")
        self.frame = None

        # Login als Startansicht festlegen
        self.switch_frame(Login(self, width=800, height=600))

    def switch_frame(self, frame_object):
        # Wechselt zur angegebenen Ansicht (Frame-Objekt).
        if self.frame is not None:
            self.frame.destroy()
        self.frame = frame_object
        if isinstance(frame_object, Register):
            self.geometry("800x1050")
        else:
            self.geometry("800x600")
        self.frame.configure(fg_color="transparent")
        self.frame.pack()


class Login(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.set_default_color_theme("green")
        title_label = ctk.CTkLabel(self, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        # Inputfelder
        self.loginname_entry = ctk.CTkEntry(self, placeholder_text="Loginname", width=400, height=50)
        self.loginname_entry.pack(pady=8, padx=20)

        password_entry = ctk.CTkEntry(self, placeholder_text="Password", width=400, height=50, show="*")
        password_entry.pack(pady=8, padx=20)

        login_button = ctk.CTkButton(self, text="Login", width=300, height=35,
                                     command=lambda: self.login(self.loginname_entry.get(), password_entry.get(),
                                                                master))
        login_button.pack(pady=16, padx=20)

        register_button = ctk.CTkButton(self, text="Register", width=200, height=35,
                                        command=lambda: master.switch_frame(Register(master)))
        register_button.pack(pady=100, padx=20)

    def login(self, login_name, passwort, master):
        if ((login_name != '') & (passwort != '')):
            self.abfrage_login(login_name, passwort, master)
        else:
            # Message an User, dass Eingabefelder befüllt werden müssen
            self.show_info("", "Gib deine vollständigen Logindaten ein.")

    def abfrage_login(self, login_name, passwort, master):

        url = f'{settings.baseUri}/login'

        # Daten, die an den Endpunkt gesendet werden sollen (als JSON)
        data = {
            "loginName": login_name,
            "passwort": {'passwort': passwort},
        }

        # Senden des POST-Requests
        response = requests.post(url, json=data)
        responseObj = response.json()
        if 'sessionID' in responseObj:
            print('Benutzer wurde erfolgreich eingeloggt.')
            master.switch_frame((FapUebersicht(master, login_name, responseObj['sessionID'])))
        else:
            self.show_warning("Fehler beim Login", "Der Loginname oder das Kennwort sind falsch.")

    def show_info(self, title, message):
        # Default messagebox for showing some information
        CTkMessagebox(title=title, message=message)

    def show_warning(self, title, warning):
        # Show some retry/cancel warnings
        msg = CTkMessagebox(title=title, message=warning,
                            icon="warning", option_1="Ok")


class Register(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ctk.set_default_color_theme("green")
        self.title_label = ctk.CTkLabel(self, text="TrackMate", font=ctk.CTkFont(size=30, weight="bold"))
        self.title_label.pack(padx=10, pady=(40, 20))
        self.configure(width=800, height=600)

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
        self.vorname_entry = ctk.CTkEntry(self, placeholder_text="Vorname", width=400, height=50)
        self.vorname_entry.pack(pady=8, padx=20)

        # Nachname Feld
        self.nachname_entry = ctk.CTkEntry(self, placeholder_text="Nachname", width=400, height=50)
        self.nachname_entry.pack(pady=8, padx=20)

        # Telefonnummer Feld
        self.telefon_entry = ctk.CTkEntry(self, placeholder_text="Telefon", width=400, height=50)
        self.telefon_entry.pack(pady=8, padx=20)

        # E-Mail-Feld mit Validierung
        email_adresse_validieren = (self.register(self.validate_mail_adresse), '%P')
        self.email_adresse_entry = ctk.CTkEntry(self, placeholder_text="E-Mail Adresse", width=400, height=50)
        self.email_adresse_entry.configure(validate='focusout', validatecommand=email_adresse_validieren)
        self.email_adresse_entry.pack(pady=8, padx=20)
        self.email_adresse_label_error = ctk.CTkLabel(self, text='E-Mail Adresse nicht gültig', text_color='red')

        # Straße Feld
        self.strasse_entry = ctk.CTkEntry(self, placeholder_text="Straße", width=400, height=50)
        self.strasse_entry.pack(pady=8, padx=20)

        # PLZ Feld
        search_ort = (self.register(self.abfrage_ort_zu_plz), '%P')
        self.plz_entry = ctk.CTkEntry(self, placeholder_text="PLZ", width=400, height=50)
        self.plz_entry.configure(validate='focusout', validatecommand=search_ort)
        self.plz_entry.pack(pady=8, padx=20)

        # Ort Feld wirt automatisch anhand der PLZ gesetzt
        self.ort_entry = ctk.CTkEntry(self, placeholder_text="Ort", width=400, height=50, state=tkinter.NORMAL)
        self.ort_entry.pack(pady=8, padx=20)

        # Land Feld
        self.land_entry = ctk.CTkEntry(self, placeholder_text="Land", width=400, height=50)
        self.land_entry.pack(pady=8, padx=20)

        # Registrierungsbutton
        register_button = ctk.CTkButton(self, text="Register", width=300, height=35,
                                        command=lambda: self.register_user(master, self.loginname_entry.get(),
                                                                           self.password_entry.get(),
                                                                           self.vorname_entry.get(),
                                                                           self.nachname_entry.get(),
                                                                           self.strasse_entry.get(),
                                                                           self.plz_entry.get(),
                                                                           self.ort_entry.get(),
                                                                           self.land_entry.get(),
                                                                           self.telefon_entry.get(),
                                                                           self.email_adresse_entry.get()))
        register_button.pack(pady=16, padx=20)

        # Schon registriert?
        already_registered_label = ctk.CTkLabel(self, text="Already registered? Than go to login!",
                                                font=ctk.CTkFont(size=14, weight="normal"))
        already_registered_label.pack(padx=10, pady=(20, 0))
        login_button = ctk.CTkButton(self, text="Login", width=300, height=35,
                                     command=lambda: master.switch_frame(Login(master)))
        login_button.pack(pady=5, padx=20)

    def validate_mail_adresse(self, mailadresse):
        # Regex dass Email mit bla@bla.bla übereinstimmt
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
        url = f'{settings.baseUri}/getOrt'

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

            self.ort_entry.insert(0, response.json()["name"])
            return response.json()["name"]
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

    def register_user(self, master, login_name, passwort, vorname, nachname, strasse, plz, ort, land, telefon,
                      email_adresse):
        # register webservice call
        print("Registering")

        # Prüfung des Benutzernamens auf Eindeutigkeit
        if self.validate_loginname(login_name):
            print("Nutzername noch nicht vorhanden")

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
                    master.switch_frame(Login(master))
                else:
                    print('Fehler beim Hinzufügen des Benutzers. Statuscode:', response.status_code)
        else:
            print("Nutzername schon vorhanden")


class FapUebersicht(ctk.CTkFrame):
    def __init__(self, master, user, session_id, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.configure(fg_color='transparent')

        # ============ Bei beiden Frames (rechts und links) erstellen ============
        self.user = user
        self.sessionID = session_id
        print('User: ', user, ' sessionID: ', session_id)
        self.positionSelbst = None
        self.positionenFreunde = []
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self, width=150, corner_radius=0)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = ctk.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============================ Linke Seite ================================
        # User suchen und auf Karte anzeigen
        self.search_user_field = ctk.CTkEntry(master=self.frame_left,
                                              placeholder_text="Benutzer suchen")
        self.search_user_field.bind("<Return>", self.standort_freund_suchen_und_auf_karte_markieren)
        self.search_user_field.grid(pady=(12, 0), padx=(20, 20), row=0, column=0)

        # Anzeigen der ausgewählten Freunde
        self.freundesNamenBox = tkinter.Listbox(master=self.frame_left, background='#343638', foreground='gray84',
                                                borderwidth=0, selectbackground='#3E454A', selectborderwidth=0,
                                                activestyle='none')
        self.freundesNamenBox.grid(pady=(10, 0), padx=(20, 20), row=1, column=0)

        self.freundEntfernen = ctk.CTkButton(master=self.frame_left,
                                             text="Freund entfernen",
                                             command=self.freund_entfernen)
        self.freundEntfernen.grid(pady=(10, 0), padx=(20, 20), row=2, column=0)

        # Eingabe der Adresse fürs Setzen als aktuellen Standort
        standort_eingabe_label = ctk.CTkLabel(master=self.frame_left, text="Standort manuell eingeben:")
        standort_eingabe_label.grid(pady=(120, 0), padx=(20, 20), row=3, column=0)

        self.land_field = ctk.CTkEntry(master=self.frame_left,
                                       placeholder_text="Land")
        self.land_field.grid(pady=(10, 0), padx=(20, 20), row=4, column=0)

        plz_update = (self.register(self.ort_fuer_plz_abfragen), '%P')
        self.plz_field = ctk.CTkEntry(master=self.frame_left,
                                      placeholder_text="PLZ")
        self.plz_field.grid(pady=(10, 0), padx=(20, 20), row=5, column=0)
        self.plz_field.configure(validate='focusout', validatecommand=plz_update)

        self.ort_field = ctk.CTkEntry(master=self.frame_left,
                                      placeholder_text="Ort")
        self.ort_field.grid(pady=(10, 0), padx=(20, 20), row=6, column=0)

        self.strasse_field = ctk.CTkEntry(master=self.frame_left,
                                          placeholder_text="Straße und Hausnr.")
        self.strasse_field.grid(pady=(10, 0), padx=(20, 20), row=7, column=0)

        self.standort_melden_button = ctk.CTkButton(master=self.frame_left,
                                                    text="Standort melden",
                                                    command=self.manuell_standort_fuer_aktuellen_user_setzen)
        self.standort_melden_button.grid(pady=(10, 20), padx=(20, 20), row=8, column=0)
        # ============================ Rechte Seite ===============================

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        # Ort auf Karte suchen
        self.standortSucheInput = ctk.CTkEntry(master=self.frame_right,
                                               placeholder_text="Standort eingeben")
        self.standortSucheInput.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.standortSucheInput.bind("<Return>", self.standort_suchen)

        self.standortSucheButton = ctk.CTkButton(master=self.frame_right,
                                                 text="Suchen",
                                                 width=90,
                                                 command=self.standort_suchen)
        self.standortSucheButton.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.logoutButton = ctk.CTkButton(master=self.frame_right, text="Logout", width=90,
                                          command=lambda: self.logout(master))
        self.logoutButton.grid(row=0, column=2, sticky='w', padx=(220, 0))

        # Karte
        self.map = mapView.TkinterMapView(self.frame_right, width=600, height=550, corner_radius=1)
        self.map.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map.add_right_click_menu_command(label="Als aktuellen Standort melden",
                                              command=self.standort_fuer_aktuellen_user_setzen, pass_coords=True)

        # eigenen Standort abfragen und in Karte markieren
        eigener_standort = self.get_standort_for_user(user)
        if eigener_standort is not None:
            self.map.set_position(eigener_standort['breitengrad'], eigener_standort['laengengrad'], 'Mein Standort',
                                  True)
            self.positionSelbst = [eigener_standort['breitengrad'], eigener_standort['laengengrad']]

        t = threading.Timer(10.0, self.karte_aktualisieren)
        t.start()

    def standort_suchen(self, event=None):
        self.map.set_address(self.standortSucheInput.get())

    def logout(self, master, event=None):
        url = f'{settings.baseUri}/logout'

        # Query-Parameter
        params = {
            "loginName": self.user,
            "sitzung": self.sessionID
        }
        # POST-Anfrage senden
        # diesmal müssen die Parameter als Body mitgeschickt werden
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(params)

        # PUT-Anfrage senden
        response = requests.post(url, data=body, headers=headers)
        print(response.json())
        # zurück zum Login
        master.switch_frame(Login(master))

    def freund_entfernen(self, event=None):
        selected_indices = self.freundesNamenBox.curselection()
        for i in selected_indices:
            # Ausgewählten Benutzer aus Box entfernen und Liste der Position der Freunde
            self.freundesNamenBox.delete(i)
            self.positionenFreunde.pop(i)

        # Karte neu laden
        self.karte_aktualisieren()

    def karte_aktualisieren(self):
        print('Karte wird neu geladen...')
        self.map.delete_all_marker()
        self.map.set_marker(self.positionSelbst[0], self.positionSelbst[1], "Mein Standort")
        for element in self.positionenFreunde:
            # Standort neu abfragen
            user_standort = self.get_standort_for_user(element[2])
            if user_standort is not None and 'breitengrad' in user_standort:
                # Standort in Klassenvariable aktualisieren
                element[0] = user_standort['breitengrad']
                element[1] = user_standort['laengengrad']
            self.map.set_marker(element[0], element[1], element[2])
        # Damit die Standorte weiterhin alle 10 Sekunden aktualisiert werden
        t = threading.Timer(10.0, self.karte_aktualisieren)
        t.start()

    def ort_fuer_plz_abfragen(self, plz):
        url = f'{settings.baseUri}/getOrt'

        # Query-Parameter
        params = {
            "postalcode": plz,
            "username": 'demo'
        }
        # GET-Anfrage senden
        response = requests.get(url, params=params)

        response_json = response.json()
        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200 and response_json is not None and 'name' in response_json:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", response_json)
            self.ort_field.delete(0, ctk.END)
            self.ort_field.insert(0, response_json['name'])
        else:
            print("Fehler bei Anfrage des Ortes zur PLZ: ", plz)
            print("Antwortinhalt: ", response_json)
        return True

    def manuell_standort_fuer_aktuellen_user_setzen(self, event=None):
        # URL des Endpunkts
        url = f'{settings.baseUri}/getStandortPerAdresse'

        # Query-Parameter
        params = {
            "login": self.user,
            "session": self.sessionID,
            "land": self.land_field.get(),
            "ort": self.ort_field.get(),
            "plz": self.plz_field.get(),
            "strasse": self.strasse_field.get()
        }
        # GET-Anfrage senden
        response = requests.get(url, params=params)

        response_json = response.json()
        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200 and response_json is not None and 'ergebnis' not in response_json:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", response_json)
            koordinaten = [response_json['breitengrad'], response_json['laengengrad']]
            self.standort_fuer_aktuellen_user_setzen(koordinaten)
        else:
            print("Fehler bei Anfrage der Koordinaten. Statuscode:", response.status_code)
            print("Antwortinhalt: ", response_json)

    def standort_fuer_aktuellen_user_setzen(self, koordinaten):
        self.map.delete_all_marker()
        self.positionSelbst = [koordinaten[0], koordinaten[1]]
        self.map.set_marker(koordinaten[0], koordinaten[1], "Mein Standort")
        for element in self.positionenFreunde:
            self.map.set_marker(element[0], element[1], element[2])

        # URL des Endpunkts
        url = f'{settings.baseUri}/setStandort'

        # Query-Parameter
        params = {
            "loginName": self.user,
            "sitzung": self.sessionID,
            "standort": {
                "breitengrad": koordinaten[0],
                "laengengrad": koordinaten[1]
            }
        }
        # diesmal müssen die Parameter als Body mitgeschickt werden
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(params)

        # PUT-Anfrage senden
        response = requests.put(url, data=body, headers=headers)

        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", response.json())
            return response.json()
        else:
            print("Fehler bei der Anfrage. Statuscode:", response.status_code)
            return None

    def standort_freund_suchen_und_auf_karte_markieren(self, event=None):
        user = self.search_user_field.get()
        userStandort = self.get_standort_for_user(user)
        if userStandort is not None and 'breitengrad' in userStandort:
            # Standort in Klassenvariable abspeichern (mit Namen des Users)
            tmpStandort = [userStandort['breitengrad'], userStandort['laengengrad'], user]
            self.positionenFreunde.append(tmpStandort)
            # In Box und auf Karte anzeigen und zur Position springen
            self.freundesNamenBox.insert('end', user)
            self.map.set_marker(userStandort['breitengrad'], userStandort['laengengrad'], text=user)
            self.map.set_position(userStandort['breitengrad'], userStandort['laengengrad'], user,
                                  True)

    def get_standort_for_user(self, user):
        # URL des Endpunkts
        url = f'{settings.baseUri}/getStandort'

        # Query-Parameter
        params = {
            "login": self.user,
            "session": self.sessionID,
            "id": user
        }
        # GET-Anfrage senden
        response = requests.get(url, params=params)

        responseJson = response.json()
        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200 and responseJson is not None and 'ergebnis' not in responseJson:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", responseJson)
            return responseJson['standort']
            # return responseJson
        else:
            print("Fehler bei Anfrage des Standorts für ", user, ". Statuscode:", response.status_code)
            print("Antwortinhalt: ", responseJson)
            return None


app = MainApp()
app.mainloop()
