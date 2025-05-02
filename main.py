import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading

# Kalendarz z dniami tygodnia
kalendarz = {
    "Poniedziałek": [],
    "Wtorek": [],
    "Środa": [],
    "Czwartek": [],
    "Piątek": []
}

# Funkcja dodająca wydarzenie
def dodaj_lekcje():
    dzien = dzien_var.get()
    godzina = godzina_var.get()
    minuta = minuta_var.get()
    przedmiot = przedmiot_entry.get()

    if not godzina or not minuta or not przedmiot:
        messagebox.showwarning("Błąd", "Wpisz godzinę, minutę i przedmiot.")
        return

    try:
        godzina_obj = datetime.strptime(f"{godzina}:{minuta}", "%H:%M")
    except ValueError:
        messagebox.showwarning("Błąd", "Niepoprawny format godziny i minut!")
        return

    kalendarz[dzien].append((godzina_obj, przedmiot))
    kalendarz[dzien].sort(key=lambda x: x[0])  # Sortowanie po godzinach
    odswiez_liste()
    przedmiot_entry.delete(0, tk.END)

# Funkcja do odświeżania listy lekcji w GUI
def odswiez_liste():
    plan_listbox.delete(0, tk.END)
    for dzien, lekcje in kalendarz.items():
        plan_listbox.insert(tk.END, f"{dzien}:")
        if lekcje:
            for i, (godzina, przedmiot) in enumerate(lekcje):
                plan_listbox.insert(tk.END, f"{i+1}. {godzina.strftime('%H:%M')} - {przedmiot}")
        else:
            plan_listbox.insert(tk.END, " Brak lekcji")
        plan_listbox.insert(tk.END, "")  # odstęp między dniami

# Funkcja usuwająca lekcję
def usun_lekcje():
    try:
        indeks = int(plan_listbox.curselection()[0]) - 1  # Przesunięcie o 1, żeby działało poprawnie
    except IndexError:
        messagebox.showwarning("Błąd", "Wybierz lekcję do usunięcia.")
        return
    except ValueError:
        messagebox.showwarning("Błąd", "Wybierz lekcję z listy.")

    dzien = dzien_var.get()

    if 0 <= indeks < len(kalendarz[dzien]):
        kalendarz[dzien].pop(indeks)
        odswiez_liste()
    else:
        messagebox.showwarning("Błąd", "Nieprawidłowy wybór lekcji.")

# Funkcja powiadamiająca o nadchodzącej lekcji
def sprawdz_lekcje():
    teraz = datetime.now()
    najblizsza_lekcja = None
    najblizsza_lekcja_dzien = ""

    for dzien, lekcje in kalendarz.items():
        for godzina, _ in lekcje:
            if godzina > teraz:
                if not najblizsza_lekcja or godzina < najblizsza_lekcja:
                    najblizsza_lekcja = godzina
                    najblizsza_lekcja_dzien = dzien

    if najblizsza_lekcja:
        czas_do_lekcji = najblizsza_lekcja - teraz
        powiadomienie_label.config(text=f"Następna lekcja: {najblizsza_lekcja.strftime('%H:%M')} ({najblizsza_lekcja_dzien})")
        countdown_label.config(text=f"Pozostały czas: {str(czas_do_lekcji).split('.')[0]}")
    else:
        powiadomienie_label.config(text="Brak zaplanowanych lekcji.")
        countdown_label.config(text="")

    # Ponowne sprawdzenie co 60 sekund
    root.after(60000, sprawdz_lekcje)

# Funkcja do pobierania i wyświetlania aktualnej godziny
def aktualna_godzina():
    teraz = datetime.now().strftime("%H:%M:%S")  # Pobranie godziny w formacie HH:MM:SS
    godzina_label.config(text=f"Aktualna godzina: {teraz}")
    root.after(1000, aktualna_godzina)  # Odświeżanie co 1 sekundę

# Funkcja do pobierania i wyświetlania dzisiejszego dnia oraz daty
def dzisiaj():
    teraz = datetime.now()
    dzien = teraz.strftime("%A")  # Dzień tygodnia
    data = teraz.strftime("%d-%m-%Y")  # Data w formacie dd-mm-yyyy
    dzien_label.config(text=f"Dzień: {dzien} | Data: {data}")
    root.after(60000, dzisiaj)  # Odświeżanie co minutę

# Uruchomienie sprawdzania lekcji w tle
def start_background_thread():
    thread = threading.Thread(target=sprawdz_lekcje)
    thread.daemon = True
    thread.start()

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Dzwonek Szkolny")
root.geometry("450x850")
root.configure(bg="#f4f4f9")

# Nagłówek
header_label = tk.Label(root, text="Dzwonek Szkolny", font=("Helvetica", 16, "bold"), bg="#f4f4f9", fg="#333")
header_label.pack(pady=20)

# Etykieta dla aktualnej godziny
godzina_label = tk.Label(root, text="Aktualna godzina: 00:00:00", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
godzina_label.pack(pady=10)

# Etykieta dla dnia i daty
dzien_label = tk.Label(root, text="Dzień: Poniedziałek | Data: 01-01-2025", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
dzien_label.pack(pady=10)

# Wybór dnia tygodnia
dzien_var = tk.StringVar(value="Poniedziałek")
tk.Label(root, text="Wybierz dzień:", bg="#f4f4f9", fg="#333").pack(pady=5)
tk.OptionMenu(root, dzien_var, *kalendarz.keys()).pack(pady=10)

# Wybór godziny
tk.Label(root, text="Wybierz godzinę:", bg="#f4f4f9", fg="#333").pack(pady=5)
godzina_var = tk.StringVar()
godzina_spinbox = tk.Spinbox(root, from_=0, to=23, textvariable=godzina_var, width=5, state="readonly")
godzina_spinbox.pack(pady=5)

# Wybór minut
tk.Label(root, text="Wybierz minutę:", bg="#f4f4f9", fg="#333").pack(pady=5)
minuta_var = tk.StringVar()
minuta_spinbox = tk.Spinbox(root, from_=0, to=59, textvariable=minuta_var, width=5, state="readonly")
minuta_spinbox.pack(pady=5)

# Wpisz przedmiot
tk.Label(root, text="Podaj przedmiot:", bg="#f4f4f9", fg="#333").pack(pady=5)
przedmiot_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
przedmiot_entry.pack(pady=10)

# Przycisk dodawania lekcji
add_button = tk.Button(root, text="Dodaj lekcję", command=dodaj_lekcje, font=("Helvetica", 12), bg="#4CAF50", fg="white")
add_button.pack(pady=10)

# Przycisk usuwania lekcji
delete_button = tk.Button(root, text="Usuń lekcję", command=usun_lekcje, font=("Helvetica", 12), bg="#f44336", fg="white")
delete_button.pack(pady=5)

# Lista z planem lekcji
plan_listbox = tk.Listbox(root, width=50, height=15, font=("Helvetica", 12), bg="#ffffff", bd=2, relief="sunken")
plan_listbox.pack(pady=10)

# Powiadomienia o nadchodzącej lekcji
powiadomienie_label = tk.Label(root, text="Następna lekcja:", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
powiadomienie_label.pack(pady=10)

# Zegar odmierzający czas do kolejnej lekcji
countdown_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f4f4f9", fg="#333")
countdown_label.pack(pady=5)

odswiez_liste()
start_background_thread()  # Uruchomienie powiadomień w tle
aktualna_godzina()  # Uruchomienie funkcji wyświetlającej aktualną godzinę
dzisiaj()  # Uruchomienie funkcji wyświetlającej dzisiejszy dzień i datę

# Uruchomienie aplikacji
root.mainloop()