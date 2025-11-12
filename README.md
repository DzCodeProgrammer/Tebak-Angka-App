# 🎮 TEBAK ANGKA PRO - The GOAT Edition ⚡

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

Aplikasi GUI number guessing game yang modern dan interaktif dengan fitur-fitur premium seperti leaderboard, achievements, statistik, dan scoring system yang kompleks!

## ✨ Fitur Utama

### 🎮 Gameplay
- **3 Level Kesulitan**: Easy (1-50), Hard (1-100), Impossible (1-200)
- **Real-time Timer**: Tracking waktu untuk bonus poin
- **Smart Hint System**: 3 hints per game dengan petunjuk strategis
- **Dynamic Scoring**: 
  - Base score dari jumlah percobaan
  - Time bonus untuk kecepatan
  - Hint bonus untuk konservasi hints
  - Level multiplier (Impossible = 3x poin!)

### 🏆 Achievements & Badges
- 💎 **Perfect Guess** - Menang dalam 1 percobaan
- ⚡ **Speedrunner** - Selesai dalam < 30 detik
- 🍀 **Lucky Seven** - Menang dalam 7 percobaan
- 😤 **Impossible Survivor** - Menang di level Impossible
- 💰 **Score Collector** - Kumpulkan 500+ poin
- 📈 **Consistency** - Menang 10 game berturut-turut

### 📊 Dashboard Statistik
- Total games & win rate
- Best time & best attempts
- Win streak tracking
- Total score accumulation
- Statistik per pemain dengan persistent storage

### 🏅 Leaderboard System
- Top 10 players ranking
- Persistent storage dengan JSON
- Data tersimpan untuk setiap pemain
- Fair scoring system

### 🎨 Modern UI/UX
- **Dark Theme Professional** - Tema gelap yang elegan
- **Smooth Animations** - Transisi warna yang smooth
- **Color-Coded System** - Warna intuitif untuk setiap status
- **Responsive Design** - Interface yang user-friendly

## 📋 Requirements

```
Python 3.8+
tkinter (biasanya sudah included dengan Python)
Windows (untuk sound effects - winsound module)
```

## 🚀 Instalasi

### Clone Repository
```bash
git clone https://github.com/DzCodeProgrammer/Tebak-Angka-App.git
cd Tebak-Angka-App
```

### Jalankan Aplikasi

**Versi Pro (Recommended):**
```bash
python tebak_angka_pro.py
```

**Versi Original:**
```bash
python tebak_angka.py
```

## 🎮 Cara Bermain

1. **Pilih Level**: Klik tombol Easy, Hard, atau Impossible
2. **Input Nama**: Masukkan nama pemain Anda
3. **Mulai Tebak**: Input angka dan tekan TEBAK atau Enter
4. **Gunakan Hints**: Klik tombol Hint untuk mendapat petunjuk
5. **Lihat Statistik**: Buka menu Statistics untuk melihat performa Anda
6. **Kompetisi**: Cek Leaderboard untuk melihat ranking top players

## 📊 Struktur Project

```
Tebak-Angka-App/
├── tebak_angka.py           # Versi original
├── tebak_angka_pro.py       # Versi modern dengan fitur lengkap
├── data/                     # Database files (auto-created)
│   ├── leaderboard.json
│   ├── stats.json
│   └── achievements.json
├── README.md
├── .gitignore
└── requirements.txt
```

## 🎯 Cara Kerja Scoring System

### Base Score
```
Base = max(100 - (percobaan * 5), 10)
```

### Time Bonus
```
TimeBonus = max(50 - waktu_dalam_detik, 0)
```

### Hint Bonus
```
HintBonus = hints_tersisa * 10
```

### Final Score
```
FinalScore = (Base + TimeBonus + HintBonus) * LevelMultiplier
- Easy: x1
- Hard: x2
- Impossible: x3
```

## 🏆 Achievement System

Unlock achievement dengan mencapai berbagai milestone:

| Achievement | Kondisi | Bonus |
|---|---|---|
| First Victory | Menang pertama kali | 🎖️ |
| Perfect Guess | Menang dalam 1 percobaan | 💎 |
| Speedrunner | Menang dalam < 30 detik | ⚡ |
| Lucky Seven | Menang dalam 7 percobaan | 🍀 |
| Impossible Survivor | Menang di level Impossible | 😤 |
| Score Collector | Kumpulkan 500+ poin | 💰 |
| Consistency | Menang 10x berturut-turut | 📈 |

## 🎨 Color Scheme

| Warna | Hex | Penggunaan |
|---|---|---|
| Primary Green | #00ffb3 | Text sukses, highlight |
| Cyan | #00d4ff | Info, judul game |
| Orange | #ffaa00 | Warning, hints |
| Red | #ff3b30 | Error, level Impossible |
| Dark | #0a0e27 | Background utama |
| Panel | #1a1f3a | Card & panel background |

## 📁 Database Files

Data disimpan dalam format JSON di folder `data/`:

### leaderboard.json
```json
{
  "PlayerName": {
    "score": 1500,
    "timestamp": "2025-11-12T10:30:45.123456"
  }
}
```

### stats.json
```json
{
  "PlayerName": {
    "total_games": 10,
    "wins": 8,
    "losses": 2,
    "total_score": 5000,
    "best_time": 25,
    "best_attempts": 2,
    "win_streak": 3,
    "max_streak": 5
  }
}
```

### achievements.json
```json
{
  "PlayerName": {
    "perfect_guess": true,
    "speedrunner": false,
    "lucky_seven": true,
    ...
  }
}
```

## ⌨️ Keyboard Shortcuts

| Tombol | Fungsi |
|---|---|
| Enter | Tebak angka |
| Escape | Close dialog |

## 🐛 Troubleshooting

### Sound tidak bekerja
- Aplikasi hanya support Windows untuk sound effects
- Jika ada error, cukup abaikan - game tetap berfungsi

### Database tidak tersimpan
- Pastikan folder `data/` ada di directory yang sama dengan script
- Cek permission folder untuk write access

### Tkinter tidak ditemukan
**Windows:**
```bash
python -m pip install tk
```

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

## 📈 Rencana Fitur Masa Depan

- [ ] Multiplayer mode dengan socket
- [ ] Custom difficulty settings
- [ ] Power-ups dan special abilities
- [ ] Seasonal leaderboard
- [ ] Export statistik ke CSV
- [ ] Dark/Light theme toggle
- [ ] Multi-language support
- [ ] Sound settings & music

## 👨‍💻 Author

**Azzikri** - The GOAT Edition Developer
- GitHub: [@DzCodeProgrammer](https://github.com/DzCodeProgrammer)
- Portfolio: [Azzikri.dev](https://azzikri.dev)

## 📝 License

Distributed under the MIT License. See LICENSE file for more information.

## 🙏 Kontribusi

Contributions are welcome! Silakan buat fork, buat branch baru, dan submit pull request.

```bash
# Fork & Clone
git clone https://github.com/YOUR_USERNAME/Tebak-Angka-App.git

# Create branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m 'Add amazing feature'

# Push to branch
git push origin feature/amazing-feature

# Create Pull Request
```

## 📞 Support

Jika ada pertanyaan atau bug report, silakan buat issue di repository ini.

---

**Made with ❤️ by Azzikri** | **The GOAT Edition** ⚡✨
