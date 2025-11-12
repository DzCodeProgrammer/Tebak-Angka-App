import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import threading
import time
import winsound
import json
import os
from datetime import datetime
from pathlib import Path

# === KONFIGURASI FILE DATABASE ===
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
LEADERBOARD_FILE = DATA_DIR / "leaderboard.json"
STATS_FILE = DATA_DIR / "stats.json"
ACHIEVEMENTS_FILE = DATA_DIR / "achievements.json"

# === VARIABEL GLOBAL ===
angka_rahasia = 0
percobaan = 0
batas = 100
skor = 0
riwayat = []
nama_pemain = "Player"
waktu_mulai = 0
hints_tersisa = 3
power_up_active = False
game_active = False
current_level = "Easy"
waktu_elapsed = 0
timer_running = False

# === ACHIEVEMENTS SYSTEM ===
ACHIEVEMENTS = {
    "first_win": {"name": "First Victory", "emoji": "🎖️", "desc": "Menang pertama kali"},
    "perfect_guess": {"name": "Perfect Guess", "emoji": "💎", "desc": "Menebak dalam 1 percobaan"},
    "speedrunner": {"name": "Speedrunner", "emoji": "⚡", "desc": "Menang dalam < 30 detik"},
    "lucky_seven": {"name": "Lucky Seven", "emoji": "🍀", "desc": "Menang dalam 7 percobaan"},
    "consistency": {"name": "Consistency", "emoji": "📈", "desc": "Menang 10 game berturut-turut"},
    "collector": {"name": "Score Collector", "emoji": "💰", "desc": "Kumpulkan 500 poin"},
    "impossible_survivor": {"name": "Impossible Survivor", "emoji": "😤", "desc": "Menang di level Impossible"},
}

# === DATABASE FUNCTIONS ===
def load_json_file(filepath):
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_json_file(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_leaderboard():
    return load_json_file(LEADERBOARD_FILE)

def save_leaderboard(data):
    save_json_file(LEADERBOARD_FILE, data)

def load_stats(player):
    stats = load_json_file(STATS_FILE)
    if player not in stats:
        stats[player] = {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "total_score": 0,
            "best_time": float('inf'),
            "best_attempts": float('inf'),
            "win_streak": 0,
            "max_streak": 0
        }
    return stats[player]

def save_stats(player, stats):
    all_stats = load_json_file(STATS_FILE)
    all_stats[player] = stats
    save_json_file(STATS_FILE, all_stats)

def load_achievements(player):
    achievements = load_json_file(ACHIEVEMENTS_FILE)
    if player not in achievements:
        achievements[player] = {ach: False for ach in ACHIEVEMENTS}
    return achievements[player]

def save_achievements(player, achievements):
    all_achievements = load_json_file(ACHIEVEMENTS_FILE)
    all_achievements[player] = achievements
    save_json_file(ACHIEVEMENTS_FILE, all_achievements)

def unlock_achievement(achievement_key):
    achievements = load_achievements(nama_pemain)
    if not achievements[achievement_key]:
        achievements[achievement_key] = True
        save_achievements(nama_pemain, achievements)
        ach = ACHIEVEMENTS[achievement_key]
        play_sound("achievement")
        messagebox.showinfo("🏆 Achievement Unlocked!", f"{ach['emoji']} {ach['name']}\n{ach['desc']}")

# === SUARA ===
def play_sound(tipe):
    try:
        if tipe == "win":
            winsound.Beep(800, 150)
            winsound.Beep(1000, 250)
        elif tipe == "lose":
            winsound.Beep(400, 200)
        elif tipe == "click":
            winsound.Beep(600, 80)
        elif tipe == "hint":
            winsound.Beep(700, 100)
        elif tipe == "achievement":
            winsound.Beep(1000, 100)
            winsound.Beep(1200, 150)
    except:
        pass

# === ANIMASI GRADIENT MODERN ===
def animate_result(widget, teks, warna_hex):
    widget.config(text=teks)
    colors = ["#1e1e1e", "#2c2c2c", "#3d3d3d", "#4e4e4e", warna_hex]
    for color in colors:
        widget.config(fg=color)
        widget.update()
        time.sleep(0.08)

# === TIMER ===
def update_timer():
    global waktu_elapsed, timer_running
    if timer_running and game_active:
        waktu_elapsed += 1
        timer_label.config(text=f"⏱️ {waktu_elapsed}s")
        root.after(1000, update_timer)

# === HINT SYSTEM ===
def give_hint():
    global hints_tersisa
    if not game_active or hints_tersisa <= 0:
        messagebox.showwarning("Oops!", "Tidak ada hints tersisa!")
        return
    
    hints_tersisa -= 1
    hint_text = f"Angka tersembunyi adalah... "
    
    if angka_rahasia < (batas // 3):
        hint_text += "di range BAWAH 👇"
    elif angka_rahasia > (batas * 2 // 3):
        hint_text += "di range ATAS 👆"
    else:
        hint_text += "di TENGAH 🎯"
    
    play_sound("hint")
    messagebox.showinfo("💡 Hint", hint_text)
    hint_button.config(text=f"💡 Hint ({hints_tersisa})")

# === MULAI GAME ===
def mulai_game(level):
    global angka_rahasia, percobaan, batas, skor, riwayat, game_active
    global nama_pemain, waktu_mulai, hints_tersisa, waktu_elapsed, timer_running
    global current_level
    
    play_sound("click")
    
    if not nama_pemain or nama_pemain == "Player":
        name = simpledialog.askstring("Siapa nama kamu?", "Masukkan nama pemain:", parent=root)
        if name:
            nama_pemain = name
            player_name_label.config(text=f"👤 {nama_pemain}")
        else:
            return
    
    percobaan = 0
    waktu_elapsed = 0
    timer_running = True
    hints_tersisa = 3
    riwayat.clear()
    game_active = True
    current_level = level
    
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
    hint_button.config(state="normal", text=f"💡 Hint ({hints_tersisa})")
    entry.delete(0, tk.END)
    entry.focus()
    
    update_timer()

# === FUNGSI TEBAK ===
def tebak():
    global percobaan, skor, game_active, stats, timer_running
    
    try:
        tebakan = int(entry.get())
        
        if tebakan < 1 or tebakan > batas:
            threading.Thread(target=animate_result, args=(hasil_label, f"⚠️ Angka harus 1–{batas}", "#ff9500")).start()
            return
        
        percobaan += 1
        riwayat.append(tebakan)
        riwayat_box.insert(tk.END, f"#{percobaan}: {tebakan}")
        play_sound("click")

        if tebakan < angka_rahasia:
            threading.Thread(target=animate_result, args=(hasil_label, "📉 Terlalu kecil!", "#ff9500")).start()
        elif tebakan > angka_rahasia:
            threading.Thread(target=animate_result, args=(hasil_label, "📈 Terlalu besar!", "#ff9500")).start()
        else:
            # MENANG!
            timer_running = False
            game_active = False
            threading.Thread(target=animate_result, args=(hasil_label, f"🎉 BENAR! Angkanya {angka_rahasia}", "#00ff7f")).start()
            play_sound("win")
            
            # Kalkulasi skor
            base_score = max(100 - (percobaan * 5), 10)
            time_bonus = max(50 - waktu_elapsed, 0)
            hint_bonus = hints_tersisa * 10
            level_multiplier = {"Easy": 1, "Hard": 2, "Impossible": 3}[current_level]
            
            frame_points = int((base_score + time_bonus + hint_bonus) * level_multiplier)
            skor += frame_points
            skor_label.config(text=f"🏆 Skor: {skor}")
            
            # Simpan stats
            stats = load_stats(nama_pemain)
            stats["total_games"] += 1
            stats["wins"] += 1
            stats["total_score"] += frame_points
            stats["best_time"] = min(stats["best_time"], waktu_elapsed)
            stats["best_attempts"] = min(stats["best_attempts"], percobaan)
            stats["win_streak"] += 1
            stats["max_streak"] = max(stats["max_streak"], stats["win_streak"])
            save_stats(nama_pemain, stats)
            
            # Update leaderboard
            leaderboard = load_leaderboard()
            leaderboard[nama_pemain] = {
                "score": skor,
                "timestamp": datetime.now().isoformat()
            }
            save_leaderboard(leaderboard)
            
            # Check achievements
            if percobaan == 1:
                unlock_achievement("perfect_guess")
            if waktu_elapsed < 30:
                unlock_achievement("speedrunner")
            if percobaan == 7:
                unlock_achievement("lucky_seven")
            if current_level == "Impossible":
                unlock_achievement("impossible_survivor")
            if stats["total_score"] >= 500:
                unlock_achievement("collector")
            
            # Tampilkan bonus points
            messagebox.showinfo("✨ Round Complete!", 
                f"Percobaan: {percobaan}\n"
                f"Waktu: {waktu_elapsed}s\n"
                f"Points: +{frame_points}\n"
                f"Total: {skor}")
            
            tombol_tebak.config(state="disabled")
            tombol_restart.config(state="normal")
    
    except ValueError:
        threading.Thread(target=animate_result, args=(hasil_label, "❌ Masukkan angka valid!", "#ff3b30")).start()
    
    entry.delete(0, tk.END)

# === LIHAT LEADERBOARD ===
def show_leaderboard():
    leaderboard = load_leaderboard()
    sorted_board = sorted(leaderboard.items(), key=lambda x: x[1]["score"], reverse=True)[:10]
    
    if not sorted_board:
        messagebox.showinfo("🏅 Leaderboard", "Belum ada data leaderboard!")
        return
    
    board_text = "🏆 TOP 10 PLAYERS 🏆\n" + "="*40 + "\n"
    for i, (player, data) in enumerate(sorted_board, 1):
        board_text += f"{i}. {player}: {data['score']} pts\n"
    
    messagebox.showinfo("🏅 Leaderboard", board_text)

# === LIHAT STATISTIK ===
def show_stats():
    stats = load_stats(nama_pemain)
    win_rate = (stats["wins"] / stats["total_games"] * 100) if stats["total_games"] > 0 else 0
    
    stats_text = (
        f"📊 STATISTIK {nama_pemain.upper()}\n"
        f"{'='*40}\n"
        f"Total Games: {stats['total_games']}\n"
        f"Wins: {stats['wins']} | Losses: {stats['losses']}\n"
        f"Win Rate: {win_rate:.1f}%\n"
        f"Total Score: {stats['total_score']}\n"
        f"Best Time: {stats['best_time']}s\n"
        f"Best Attempts: {stats['best_attempts']}\n"
        f"Win Streak: {stats['win_streak']} (Max: {stats['max_streak']})"
    )
    messagebox.showinfo("📊 Statistik", stats_text)

# === LIHAT ACHIEVEMENTS ===
def show_achievements():
    achievements = load_achievements(nama_pemain)
    unlocked = sum(1 for v in achievements.values() if v)
    
    ach_text = f"🏅 ACHIEVEMENTS ({unlocked}/{len(ACHIEVEMENTS)})\n{'='*40}\n"
    for key, ach in ACHIEVEMENTS.items():
        status = "✅" if achievements.get(key, False) else "🔒"
        ach_text += f"{status} {ach['emoji']} {ach['name']}\n"
    
    messagebox.showinfo("🏅 Achievements", ach_text)

# === RESTART ===
def restart_game():
    mulai_game(current_level)

# === SETUP WINDOW ===
root = tk.Tk()
root.title("🎮 TEBAK ANGKA PRO - Azzikri Edition ⚡")
root.geometry("700x850")
root.config(bg="#0a0e27")
root.resizable(False, False)

# === HEADER ===
header_frame = tk.Frame(root, bg="#1a1f3a", height=80)
header_frame.pack(fill="x", padx=0, pady=0)
header_frame.pack_propagate(False)

judul = tk.Label(header_frame, text="🎮 TEBAK ANGKA PRO ⚡", font=("Poppins", 26, "bold"), 
                 fg="#00d4ff", bg="#1a1f3a")
judul.pack(pady=(10, 0))

player_name_label = tk.Label(header_frame, text="👤 Player", font=("Poppins", 11), 
                             fg="#00ffb3", bg="#1a1f3a")
player_name_label.pack()

# === TOP STATS BAR ===
top_bar = tk.Frame(root, bg="#0a0e27")
top_bar.pack(fill="x", padx=15, pady=10)

skor_label = tk.Label(top_bar, text="🏆 Skor: 0", font=("Poppins", 14, "bold"), 
                      fg="#00ffb3", bg="#0a0e27")
skor_label.pack(side="left", padx=10)

timer_label = tk.Label(top_bar, text="⏱️ 0s", font=("Poppins", 14, "bold"), 
                       fg="#ff9500", bg="#0a0e27")
timer_label.pack(side="right", padx=10)

# === LEVEL SELECTION ===
level_frame = tk.Frame(root, bg="#0a0e27")
level_frame.pack(pady=10)

tk.Label(level_frame, text="Pilih Level:", font=("Poppins", 11, "bold"), 
         fg="#cccccc", bg="#0a0e27").pack()

buttons_frame = tk.Frame(level_frame, bg="#0a0e27")
buttons_frame.pack(pady=5)

for lvl, color in [("Easy", "#00ff88"), ("Hard", "#ffaa00"), ("Impossible", "#ff3b30")]:
    btn = tk.Button(
        buttons_frame,
        text=lvl,
        font=("Poppins", 11, "bold"),
        bg="#1a1f3a",
        fg=color,
        activebackground=color,
        activeforeground="#0a0e27",
        relief="flat",
        width=12,
        command=lambda l=lvl: mulai_game(l),
        bd=2,
        highlightthickness=1,
        highlightbackground=color
    )
    btn.pack(side="left", padx=8, pady=5)

# === GAME FRAME ===
game_frame = tk.Frame(root, bg="#1a1f3a", bd=3, relief="ridge")
game_frame.pack(padx=15, pady=15, fill="both", expand=True)

entry = tk.Entry(game_frame, font=("Poppins", 28, "bold"), justify="center", 
                bg="#2c3a5a", fg="#00ffb3", relief="flat", width=4, insertbackground="#00ffb3")
entry.pack(pady=20, ipady=15)

tombol_tebak = tk.Button(game_frame, text="🎯 TEBAK!", font=("Poppins", 16, "bold"), 
                        bg="#00d4ff", fg="white",
                        activebackground="#00ffb3", activeforeground="#0a0e27", 
                        relief="flat", command=tebak, state="disabled", cursor="hand2")
tombol_tebak.pack(pady=10, ipadx=15, ipady=8)

hasil_label = tk.Label(game_frame, text="🎯 Pilih level untuk mulai!", 
                      font=("Poppins", 15, "bold"), fg="#00bcd4", bg="#1a1f3a", wraplength=350)
hasil_label.pack(pady=15)

# === HINT BUTTON ===
hint_button = tk.Button(game_frame, text="💡 Hint (3)", font=("Poppins", 11, "bold"),
                       bg="#2c3a5a", fg="#ffaa00", activebackground="#ffaa00",
                       activeforeground="#0a0e27", relief="flat", state="disabled",
                       command=give_hint, cursor="hand2")
hint_button.pack(pady=5)

# === HISTORY ===
history_label = tk.Label(root, text="📝 Riwayat Tebakan", font=("Poppins", 11, "bold"), 
                        fg="#00ffb3", bg="#0a0e27")
history_label.pack(anchor="w", padx=15, pady=(10, 5))

riwayat_box = tk.Listbox(root, bg="#1a1f3a", fg="#00ffb3", font=("Consolas", 10), 
                         height=4, width=50, bd=0, relief="flat", 
                         selectmode="none", highlightthickness=0)
riwayat_box.pack(padx=15, pady=(0, 10), fill="both", expand=True)

# === BUTTONS ===
button_frame = tk.Frame(root, bg="#0a0e27")
button_frame.pack(fill="x", padx=15, pady=10)

tombol_restart = tk.Button(button_frame, text="🔁 Main Lagi", font=("Poppins", 12, "bold"), 
                           bg="#1a1f3a", fg="#00ffb3", activebackground="#00ffb3",
                           activeforeground="#0a0e27", relief="flat", state="disabled",
                           command=restart_game, cursor="hand2", bd=2, highlightthickness=1,
                           highlightbackground="#00ffb3")
tombol_restart.pack(side="left", padx=5, ipadx=10, ipady=5)

leaderboard_btn = tk.Button(button_frame, text="🏅 Leaderboard", font=("Poppins", 12, "bold"),
                            bg="#1a1f3a", fg="#ffaa00", activebackground="#ffaa00",
                            activeforeground="#0a0e27", relief="flat", command=show_leaderboard,
                            cursor="hand2", bd=2, highlightthickness=1, highlightbackground="#ffaa00")
leaderboard_btn.pack(side="left", padx=5, ipadx=10, ipady=5)

stats_btn = tk.Button(button_frame, text="📊 Statistik", font=("Poppins", 12, "bold"),
                     bg="#1a1f3a", fg="#00bcd4", activebackground="#00bcd4",
                     activeforeground="#0a0e27", relief="flat", command=show_stats,
                     cursor="hand2", bd=2, highlightthickness=1, highlightbackground="#00bcd4")
stats_btn.pack(side="left", padx=5, ipadx=10, ipady=5)

achievements_btn = tk.Button(button_frame, text="🏆 Achievements", font=("Poppins", 12, "bold"),
                             bg="#1a1f3a", fg="#ff7700", activebackground="#ff7700",
                             activeforeground="#0a0e27", relief="flat", command=show_achievements,
                             cursor="hand2", bd=2, highlightthickness=1, highlightbackground="#ff7700")
achievements_btn.pack(side="left", padx=5, ipadx=10, ipady=5)

# === FOOTER ===
footer = tk.Label(root, text="✨ Made by Azzikri | The GOAT Edition ✨", 
                 font=("Poppins", 9), fg="#666666", bg="#0a0e27")
footer.pack(side="bottom", pady=8)

# === BIND ENTER KEY ===
entry.bind("<Return>", lambda e: tebak())

root.mainloop()
