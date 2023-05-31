import customtkinter as ctk
import requests

from register import Register
import tkintermapview as mapView

import settings
import json


# let the fun begin!
class FapUebersicht(ctk.CTkFrame):
    def __init__(self, master, user, sessionId, **kwargs):
        super().__init__(master, **kwargs)

        # title_image = ctk.CTkImage(Image.open("TrackMate Logo.png"), size=(50, 50))

        # ============ Bei beiden Frames (rechts und links) erstellen ============
        self.user = user
        self.sessionID = sessionId
        print('User: ', user, ' sessionID: ', sessionId)
        self.positionSelbst = None
        self.positionenFreunde = []
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = ctk.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============================ Linke Seite ================================
        # self.frame_left.grid_rowconfigure(2, weight=1)
        self.search_user_field = ctk.CTkEntry(master=self.frame_left,
                                              placeholder_text="Benutzer suchen")
        self.search_user_field.bind("<Return>", self.standortFreundSuchenUndAufKarteMarkieren)
        self.search_user_field.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.freundeNamensliste = ctk.CTkLabel(master=self.frame_left, text="test\ntest")
        self.freundeNamensliste.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        # Eingabe der Adresse
        self.land_field = ctk.CTkEntry(master=self.frame_left,
                                       placeholder_text="Land")
        self.land_field.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        self.ort_field = ctk.CTkEntry(master=self.frame_left,
                                      placeholder_text="Ort")
        self.ort_field.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)

        self.plz_field = ctk.CTkEntry(master=self.frame_left,
                                      placeholder_text="PLZ")
        self.plz_field.grid(pady=(20, 0), padx=(20, 20), row=4, column=0)

        self.strasse_field = ctk.CTkEntry(master=self.frame_left,
                                          placeholder_text="Straße und Hausnr.")
        self.strasse_field.grid(pady=(20, 0), padx=(20, 20), row=5, column=0)

        self.standort_melden_button = ctk.CTkButton(master=self.frame_left,
                                                    text="Standort melden",
                                                    command=self.manuellStandortFuerAktuellenUserSetzen)
        self.standort_melden_button.grid(pady=(20, 0), padx=(20, 20), row=6, column=0)
        # ============================ Rechte Seite ===============================

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.standortSucheInput = ctk.CTkEntry(master=self.frame_right,
                                               placeholder_text="Standort eingeben")
        self.standortSucheInput.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.standortSucheInput.bind("<Return>", self.standortSuchen)

        self.standortSucheButton = ctk.CTkButton(master=self.frame_right,
                                                 text="Suchen",
                                                 width=90,
                                                 command=self.standortSuchen)
        self.standortSucheButton.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.map = mapView.TkinterMapView(self.frame_right, width=600, height=400, corner_radius=1)
        self.map.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        # map.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map.add_right_click_menu_command(label="Als aktuellen Standort melden",
                                              command=self.standortFuerAktuellenUserSetzen, pass_coords=True)
        # setStandortFuerAktuellenUser(self)
        eigener_standort = self.getStandortForUser(user)
        # eigener_standort = None
        if eigener_standort is not None:
            # map.set_marker(eigener_standort['breitengrad'], eigener_standort['laengengrad'], text="Eigene Position")
            self.map.set_position(eigener_standort['breitengrad'], eigener_standort['laengengrad'], 'Mein Standort',
                                  True)

    def standortSuchen(self, event=None):
        self.map.set_address(self.standortSucheInput.get())

    def manuellStandortFuerAktuellenUserSetzen(self, event=None):
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
        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200 and response_json is not None and 'ergebnis' not in response_json:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", response_json)
            koordinaten = [response_json['breitengrad'], response_json['laengengrad']]
            self.standortFuerAktuellenUserSetzen(koordinaten)
        else:
            print("Fehler bei Anfrage der Koordinaten. Statuscode:", response.status_code)
            print("Antwortinhalt: ", response_json)

    def standortFuerAktuellenUserSetzen(self, koordinaten):
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
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(params)

        # PUT-Anfrage senden
        response = requests.put(url, data=body, headers=headers)

        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", response.json())
            return response.json()
        else:
            print("Fehler bei der Anfrage. Statuscode:", response.status_code)
            return None

    def standortFreundSuchenUndAufKarteMarkieren(self, event=None):
        user = self.search_user_field.get()
        userStandort = self.getStandortForUser(user)
        if userStandort is not None and 'breitengrad' in userStandort:
            tmpStandort = [userStandort['breitengrad'], userStandort['laengengrad'], user]
            self.positionenFreunde.append(tmpStandort)
            self.map.set_marker(userStandort['breitengrad'], userStandort['laengengrad'], text=user)
            self.map.set_position(userStandort['breitengrad'], userStandort['laengengrad'], user,
                                  True)

    def getStandortForUser(self, user):
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
        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200 and responseJson is not None and 'ergebnis' not in responseJson:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", responseJson)
            return responseJson['standort']
            # return responseJson
        else:
            print("Fehler bei Anfrage des Standorts für ", user, ". Statuscode:", response.status_code)
            print("Antwortinhalt: ", responseJson)
            return None
