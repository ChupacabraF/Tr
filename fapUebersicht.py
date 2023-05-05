import customtkinter as ctk
import requests

from register import Register
import tkintermapview as mapView


# let the fun begin!
class FapUebersicht(ctk.CTkFrame):
    def __init__(self, master, user, sessionId, **kwargs):
        super().__init__(master, **kwargs)

        # title_image = ctk.CTkImage(Image.open("TrackMate Logo.png"), size=(50, 50))

        # ============ Bei beiden Frames (rechts und links) erstellen ============

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
        self.search_user_field.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

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
        eigenerStandort = getStandortForUser(user, sessionId)
        # eigenerStandort = None
        if eigenerStandort is not None:
            # map.set_marker(eigenerStandort['breitengrad'], eigenerStandort['laengengrad'], text="Eigene Position")
            self.map.set_position(eigenerStandort['breitengrad'], eigenerStandort['laengengrad'], 'Eigene Position',
                                  True)

    def standortSuchen(self, event=None):
        self.map.set_address(self.standortSucheInput.get())

    def standortFuerAktuellenUserSetzen(self, koordinaten):
        self.map.delete_all_marker()
        self.positionSelbst = self.map.set_marker(koordinaten[0], koordinaten[1], "Mein Standort")
        for element in self.positionenFreunde:
            self.map.set_marker(element[0], element[1], element[2])

        # URL des Endpunkts
        url = "https://fapfa.azurewebsites.net/FAPServer/service/fapservice/setStandort"

        # Query-Parameter
        params = {
            "loginName": "rainer",
            "sitzung": "8315c3e0-41d6-4ed7-a10c-7ca14cea5abe",
            "standort": {
                "breitengrad": koordinaten[0],
                "laengengrad": koordinaten[1]
            }
        }
        # GET-Anfrage senden
        response = requests.get(url, params=params)

        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            # Antwortinhalt als JSON ausgeben
            print("Antwortinhalt: ", response.json())
            return response.json()
        else:
            print("Fehler bei der Anfrage. Statuscode:", response.status_code)
            return None


def getStandortForUser(user, sessionId):
    # URL des Endpunkts
    url = "https://fapfa.azurewebsites.net/FAPServer/service/fapservice/getStandort"

    # Query-Parameter
    params = {
        "login": user,
        "session": sessionId
    }
    # GET-Anfrage senden
    response = requests.get(url, params=params)

    responseJson = response.json()
    # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
    if response.status_code == 200 and 'ergebnis' not in responseJson:
        # Antwortinhalt als JSON ausgeben
        print("Antwortinhalt: ", responseJson)
        return responseJson
    else:
        print("Fehler bei Anfrage des Standorts für ", user, ". Statuscode:", response.status_code)
        print("Antwortinhalt: ", responseJson)
        return None
