import tkinter as tk
from tkinter import messagebox
import random
from collections import namedtuple
from main import main

Point = namedtuple('Point', ['x', 'y'])

# funkcja losująca 100 punktów
def Losuj100():
    points = [Point(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(100)]
    wynik = main(points, canvas_frame)
    typ_wierzcholki.config(text=wynik)
    okno.geometry("900x700")

# funkcja pobierająca punkty od użytkownika
def PobierzPunkty():
    text = punkty_text.get("1.0", tk.END).strip()
    points = []
    try:
        for line in text.splitlines():
            x_str, y_str = line.strip().split()
            x, y = float(x_str), float(y_str)
            points.append(Point(x, y))
        if len(points) < 3:
            raise ValueError("Potrzeba przynajmniej 3 punktów.")
        wynik = main(points, canvas_frame)
        typ_wierzcholki.config(text=wynik)
        okno.geometry("900x700")
    except Exception:
        messagebox.showerror("Błąd", "Upewnij się, że wpisujesz punkty w formacie: x y (każdy w nowej linii, min. 3 punkty)")

# GUI aplikacji
okno = tk.Tk()
okno.geometry("700x400")
okno.title("Otoczka wypukła")

glowna_ramka = tk.Frame(okno)
glowna_ramka.pack(fill="both", expand=True, padx=10, pady=10)

lewa_kolumna = tk.Frame(glowna_ramka)
lewa_kolumna.pack(side="left", anchor="n", fill="y")

prawa_kolumna = tk.Frame(glowna_ramka)
prawa_kolumna.pack(side="right", anchor="n", fill="y")

wprowadz_punkty = tk.Label(lewa_kolumna, text="Wprowadź punkty (x y):")
wprowadz_punkty.pack(anchor='w', padx=10, pady=(10, 5))

punkty_text = tk.Text(lewa_kolumna, height=10, width=30)
punkty_text.pack(padx=10, pady=5)

przycisk_ręczny = tk.Button(lewa_kolumna, text="Rysuj otoczkę", command=PobierzPunkty)
przycisk_ręczny.pack(pady=10)

otoczka100_label = tk.Label(prawa_kolumna, text="Otoczka 100 losowych punktów\n(zakres: -100 do 100)", justify="left")
otoczka100_label.pack(padx=10, pady=(10, 5))

otoczka100_button = tk.Button(prawa_kolumna, text="Rysuj otoczkę", command=Losuj100)
otoczka100_button.pack(pady=10)

typ_wierzcholki = tk.Label(okno, text="", justify="left", font=("Arial", 10), fg="black")
typ_wierzcholki.pack(pady=(5, 10))

canvas_frame = tk.Frame(okno)
canvas_frame.pack(fill="both", expand=True)

okno.mainloop()
