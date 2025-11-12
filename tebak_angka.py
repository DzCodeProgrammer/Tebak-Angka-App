import tkinter as tk
import random
import threading
import time
import winsound  # untuk efek suara (Windows)

# === Variabel Global ===
angka_rahasia = 0
percobaan = 0
batas = 100
skor = 0
riwayat = []

# === FUNGSI ANIMASI FADE-IN ===
def fade_in(widget, teks, warna="#00ffb3"):
    widget.config(fg=warna)
    for i in range(0, 11):
        widget.config(fg=f"#{int(i*25):02x}{255-int(i*25):02x}{179-int(i*12):02x}")
        widget.update()
        time.sleep(0.02)
    widget.config(text=teks)

# === SUARA ===
def play_sound(tipe):
    if tipe == "win":
        winsound.Beep(800, 150)
        winsound.Beep(1000, 250)
    elif tipe == "lose":
        winsound.Beep(400, 200)
    elif tipe == "click":
        winsound.Beep(600, 80)

# === MULAI GAME ===
def mulai_game(level):
    global angka_rahasia, percobaan, batas, skor, riwayat
    play_sound("click")
    percobaan = 0
    riwayat.clear()
    riwayat_box.delete(0, tk.END)
    if level == "Easy":
        batas = 50
    elif level == "Hard":
        batas = 100
    else:
        batas = 200
    angka_rahasia = random.randint(1, batas)
    hasil_label.config(text=f"🎯 Tebak angka 1–{batas}", fg="#00bcd4")
    tombol_tebak.config(state="normal")
    tombol_restart.config(state="disabled")
    entry.delete(0, tk.END)

# === FUNGSI TEBAK ===
def tebak():
    global percobaan, skor
    try:
        tebakan = int(entry.get())
        percobaan += 1
        riwayat.append(tebakan)
        riwayat_box.insert(tk.END, f"Percobaan {percobaan}: {tebakan}")
        play_sound("click")

        if tebakan < angka_rahasia:
            threading.Thread(target=fade_in, args=(hasil_label, "📉 Terlalu kecil", "#ffaa00")).start()
        elif tebakan > angka_rahasia:
            threading.Thread(target=fade_in, args=(hasil_label, "📈 Terlalu besar", "#ffaa00")).start()
        else:
            threading.Thread(target=fade_in, args=(hasil_label, f"🎉 Benar! Angkanya {angka_rahasia}", "#00ff7f")).start()
            play_sound("win")
            skor += max(10 - (percobaan // 2), 1)
            skor_label.config(text=f"🏆 Skor: {skor}")
            tombol_tebak.config(state="disabled")
            tombol_restart.config(state="normal")
    except ValueError:
        threading.Thread(target=fade_in, args=(hasil_label, "Masukkan angka valid!", "#ff3b30")).start()
    entry.delete(0, tk.END)

# === RESTART ===
def restart_game():
    mulai_game("Easy")

# === SETUP WINDOW ===
root = tk.Tk()
root.title("🎮 Tebak Angka Super Modern - Azzikri Edition")
root.geometry("500x650")
root.config(bg="#121212")
root.resizable(False, False)

# === JUDUL ===
judul = tk.Label(root, text="Tebak Angka Super Modern ⚡", font=("Poppins", 24, "bold"), fg="#00ffb3", bg="#121212")
judul.pack(pady=(20, 5))

subjudul = tk.Label(root, text="Pilih level lalu mulai permainan!", font=("Poppins", 11), fg="#cccccc", bg="#121212")
subjudul.pack(pady=(0, 20))

# === SKOR ===
skor_label = tk.Label(root, text="🏆 Skor: 0", font=("Poppins", 13, "bold"), fg="#00bcd4", bg="#121212")
skor_label.pack(pady=(0, 10))

# === FRAME LEVEL ===
frame_level = tk.Frame(root, bg="#121212")
frame_level.pack(pady=5)

for lvl in ["Easy", "Hard", "Impossible"]:
    btn = tk.Button(
        frame_level,
        text=lvl,
        font=("Poppins", 12, "bold"),
        bg="#2c2c2c",
        fg="#00ffb3",
        activebackground="#00ffb3",
        activeforeground="#121212",
        relief="flat",
        width=10,
        command=lambda l=lvl: mulai_game(l)
    )
    btn.pack(side="left", padx=10)

# === FRAME GAME ===
frame = tk.Frame(root, bg="#1e1e1e", bd=4, relief="ridge")
frame.pack(padx=20, pady=20, fill="both")

entry = tk.Entry(frame, font=("Poppins", 20, "bold"), justify="center", bg="#2c2c2c", fg="#00ffb3", relief="flat", width=5)
entry.pack(pady=20)

tombol_tebak = tk.Button(frame, text="TEBAK!", font=("Poppins", 18, "bold"), bg="#00bcd4", fg="white",
                         activebackground="#00ffb3", activeforeground="#121212", relief="flat", command=tebak)
tombol_tebak.pack(pady=10, ipadx=10, ipady=5)

hasil_label = tk.Label(frame, text="🎯 Belum mulai, pilih level dulu", font=("Poppins", 14), fg="#00bcd4", bg="#1e1e1e")
hasil_label.pack(pady=20)

# === LISTBOX RIWAYAT ===
riwayat_box = tk.Listbox(root, bg="#1e1e1e", fg="#00ffb3", font=("Consolas", 11), height=8, width=45, bd=0, relief="flat")
riwayat_box.pack(pady=10)

# === TOMBOL RESTART ===
tombol_restart = tk.Button(root, text="Main Lagi 🔁", font=("Poppins", 14, "bold"), bg="#2c2c2c", fg="#ffffff",
                           activebackground="#00ffb3", activeforeground="#121212", relief="flat", state="disabled",
                           command=restart_game)
tombol_restart.pack(pady=(15, 20), ipadx=8, ipady=4)

# === FOOTER ===
footer = tk.Label(root, text="Made by Azzikri ✨", font=("Poppins", 10), fg="#888888", bg="#121212")
footer.pack(side="bottom", pady=10)

root.mainloop()
