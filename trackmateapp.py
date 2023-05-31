import customtkinter as ctk
from login import Login
from fapUebersicht import FapUebersicht


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Hauptfenster der Anwendung konfigurieren
        self.title("TrackMate")
        self.geometry("800x600")
        # self.set_default_color_theme("green")

        # View 1 als Startansicht festlegen
        self.frame = None
        # self.current_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.switch_frame(Login(self))
        # self.switch_frame(FapUebersicht)

    def switch_frame(self, frame_object):
        # Wechselt zur angegebenen Ansicht (Frame-Objekt).
        if self.frame is not None:
            self.frame.destroy()
        self.frame = frame_object
        self.frame.pack()


app = MainApp()
app.mainloop()
