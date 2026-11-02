from swe_installer import paths, constants

from customtkinter import CTk

app = CTk

def create_app():
    global app

    app = CTk("#0f0f11")
    app.geometry("800x600")
    app.title(f"{constants.APP_NAME} Installer")

def main():
    create_app()

    app.mainloop()