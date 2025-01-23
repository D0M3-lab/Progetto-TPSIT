import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class BilancioNegozio:
    def __init__(self, file_nome="bilancio.json"):
        self.file_nome = file_nome
        self.transazioni = self.carica_transazioni()

    def carica_transazioni(self):
        try:
            with open(self.file_nome, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salva_transazioni(self):
        with open(self.file_nome, 'w') as file:
            json.dump(self.transazioni, file, indent=4)

    def aggiungi_transazione(self, tipo, descrizione, importo):
        if tipo not in ['entrata', 'uscita']:
            raise ValueError("Tipo di transazione non valido! Deve essere 'entrata' o 'uscita'.")
        transazione = {
            'tipo': tipo,
            'descrizione': descrizione,
            'importo': importo
        }
        self.transazioni.append(transazione)
        self.salva_transazioni()

    def elimina_transazione(self, indice):
        if indice < 0 or indice >= len(self.transazioni):
            raise IndexError("Indice di transazione non valido.")
        del self.transazioni[indice]
        self.salva_transazioni()

    def modifica_transazione(self, indice, tipo, descrizione, importo):
        if indice < 0 or indice >= len(self.transazioni):
            raise IndexError("Indice di transazione non valido.")
        if tipo not in ['entrata', 'uscita']:
            raise ValueError("Tipo di transazione non valido! Deve essere 'entrata' o 'uscita'.")
        self.transazioni[indice] = {
            'tipo': tipo,
            'descrizione': descrizione,
            'importo': importo
        }
        self.salva_transazioni()

    def calcola_bilancio(self):
        entrate = sum(t['importo'] for t in self.transazioni if t['tipo'] == 'entrata')
        uscite = sum(t['importo'] for t in self.transazioni if t['tipo'] == 'uscita')
        return entrate - uscite

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Bilancio")
        self.root.geometry("720x720")
        self.root.configure(bg="#1e1e2f")

        self.negozio = BilancioNegozio()

        # Header
        self.header_frame = tk.Frame(root, bg="#2b2b3c", pady=10)
        self.header_frame.pack(fill=tk.X)
        self.bilancio_label = tk.Label(self.header_frame, text=f"Bilancio: {self.negozio.calcola_bilancio()}€", font=("Arial", 20), fg="#ffffff", bg="#2b2b3c")
        self.bilancio_label.pack()

        # Body
        self.body_frame = tk.Frame(root, bg="#1e1e2f", pady=10)
        self.body_frame.pack(fill=tk.BOTH, expand=True)

        self.transazioni_canvas = tk.Canvas(self.body_frame, bg="#1e1e2f", highlightthickness=0)
        self.transazioni_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.transazioni_frame = tk.Frame(self.transazioni_canvas, bg="#1e1e2f")
        self.transazioni_canvas.create_window((0, 0), window=self.transazioni_frame, anchor="nw")
        self.transazioni_frame.bind("<Configure>", lambda e: self.transazioni_canvas.configure(scrollregion=self.transazioni_canvas.bbox("all")))

        self.aggiorna_lista_transazioni()

        # Footer
        self.footer_frame = tk.Frame(root, bg="#2b2b3c", pady=10)
        self.footer_frame.pack(fill=tk.X)

        tk.Button(self.footer_frame, text="Aggiungi Transazione", command=self.aggiungi_transazione, bg="#404056", fg="#ffffff", font=("Arial", 12), pady=5, padx=10).pack(side=tk.LEFT, padx=10)

    def aggiorna_bilancio(self):
        bilancio = self.negozio.calcola_bilancio()
        bilancio_text = f"Bilancio: {bilancio}€"

        # Se il bilancio è negativo, il colore del testo diventa rosso, altrimenti bianco
        bilancio_fg = "E4080A" if bilancio < 0 else "ffffff"

        # Aggiorna la label del bilancio
        self.bilancio_label.config(text=bilancio_text, fg=bilancio_fg)

    def aggiorna_lista_transazioni(self):
        for widget in self.transazioni_frame.winfo_children():
            widget.destroy()

        colors = ["#f39c12", "#e74c3c", "#8e44ad", "#3498db"]

        for i, t in enumerate(self.negozio.transazioni):
            color = colors[i % len(colors)]
            frame = tk.Frame(self.transazioni_frame, bg="#2b2b3c", pady=10, padx=10)
            frame.pack(fill=tk.X, pady=5, padx=5)

            canvas = tk.Canvas(frame, width=30, height=30, bg="#2b2b3c", highlightthickness=0)
            canvas.grid(row=0, column=0, rowspan=2, padx=5)
            canvas.create_oval(5, 5, 25, 25, fill=color, outline=color)

            tk.Label(frame, text=t['tipo'].capitalize(), font=("Arial", 14, "bold"), bg="#2b2b3c", fg="#ffffff").grid(row=0, column=1, sticky="w")
            tk.Label(frame, text=t['descrizione'], font=("Arial", 12), bg="#2b2b3c", fg="#b4b4b4").grid(row=1, column=1, sticky="w")
            tk.Label(frame, text=f"{t['importo']}€", font=("Arial", 14), bg="#2b2b3c", fg="#ffffff").grid(row=0, column=2, rowspan=2, sticky="e", padx=10)

            # Box for buttons placed beside the transaction
            button_frame = tk.Frame(frame, bg="#2b2b3c")
            button_frame.grid(row=0, column=3, rowspan=2, padx=10, sticky="e")

            # Modify button
            tk.Button(button_frame, text="Modifica", command=lambda i=i: self.modifica_transazione(i), bg="#404056", fg="#ffffff", font=("Arial", 9), pady=3, padx=8).pack(side=tk.TOP, pady=3)

            # Eliminate button (in red)
            tk.Button(button_frame, text="Elimina", command=lambda i=i: self.elimina_transazione(i), bg="#e74c3c", fg="#ffffff", font=("Arial", 9), pady=3, padx=8).pack(side=tk.TOP, pady=3)

    def aggiungi_transazione(self):
        tipo = simpledialog.askstring("Aggiungi Transazione", "Tipo di transazione (entrata/uscita):")
        descrizione = simpledialog.askstring("Aggiungi Transazione", "Descrizione della transazione:")
        importo = simpledialog.askfloat("Aggiungi Transazione", "Importo della transazione:")

        if tipo and descrizione and importo is not None:
            try:
                self.negozio.aggiungi_transazione(tipo, descrizione, importo)
                messagebox.showinfo("Successo", "Transazione aggiunta con successo!")
                self.aggiorna_bilancio()
                self.aggiorna_lista_transazioni()
            except ValueError as e:
                messagebox.showerror("Errore", str(e))
        else:
            messagebox.showerror("Errore", "Dati non validi o incompleti.")


    def modifica_transazione(self, indice):
        transazione = self.negozio.transazioni[indice]
        tipo = simpledialog.askstring("Modifica Transazione", f"Tipo di transazione ({transazione['tipo']}):", initialvalue=transazione['tipo'])
        descrizione = simpledialog.askstring("Modifica Transazione", f"Descrizione ({transazione['descrizione']}):", initialvalue=transazione['descrizione'])
        importo = simpledialog.askfloat("Modifica Transazione", f"Importo ({transazione['importo']}):", initialvalue=transazione['importo'])

        if tipo and descrizione and importo is not None:
            try:
                self.negozio.modifica_transazione(indice, tipo, descrizione, importo)
                messagebox.showinfo("Successo", "Transazione modificata con successo!")
                self.aggiorna_bilancio()
                self.aggiorna_lista_transazioni()
            except ValueError as e:
                messagebox.showerror("Errore", str(e))
        else:
            messagebox.showerror("Errore", "Dati non validi o incompleti.")

    def elimina_transazione(self, indice):
        try:
            self.negozio.elimina_transazione(indice)
            messagebox.showinfo("Successo", "Transazione eliminata con successo!")
            self.aggiorna_bilancio()
            self.aggiorna_lista_transazioni()
        except IndexError as e:
            messagebox.showerror("Errore", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
