import customtkinter as ctk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppFitness(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fitness App")
        self.geometry("500x600")

        self.label = ctk.CTkLabel(self, text="GENERADOR DE PLAN", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre", width=250)
        self.entry_nombre.pack(pady=10)

        self.entry_peso = ctk.CTkEntry(self, placeholder_text="Peso (kg)", width=250)
        self.entry_peso.pack(pady=10)

        self.btn = ctk.CTkButton(self, text="Generar PDF", command=self.generar)
        self.btn.pack(pady=20)

    def generar(self):
        nombre = self.entry_nombre.get()
        if not nombre:
            messagebox.showerror("Error", "Escribe un nombre")
            return
        
        archivo = f"Plan_{nombre}.pdf"
        doc = SimpleDocTemplate(archivo, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph(f"Plan para: {nombre}", styles['Title'])]
        doc.build(story)
        
        messagebox.showinfo("Listo", f"PDF creado: {archivo}")
        os.startfile(archivo)

if __name__ == "__main__":
    app = AppFitness()
    app.mainloop()