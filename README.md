# 🤖 Aqlli Savol-Javob va Test Tahlilchi Telegram Bot

Foydalanuvchilar yuborgan bitta yoki bir nechta savollarni (matn va rasm ko'rinishida) qabul qiluvchi, AI yordamida chuqur tahlil qilib, to'g'ri javoblarni asosli izohlar bilan chiroyli formatda chiqarib beruvchi Telegram bot.

Loyiha **Python 3.10+** va **aiogram 3.x** asosida modulli arxitekturada yaratilgan.
Tashqi murakkab API kalitlar shart emas — bot to'liq mustaqil va bepul ishlaydi!

---

## 🌟 Asosiy Imkoniyatlar

- **Oddiy va nazariy savollar:** Istalgan fandan berilgan savolni tahlil qilib, to'g'ri javob va uning tushunarli izohini beradi.
- **Bir vaqtda bir nechta savolni tahlil qilish:** Foydalanuvchi bir nechta savollarni bitta xabarda yuborsa, bot har birini alohida ajratib, tartibli tahlil qiladi.
- **Variantli testlar (A, B, C, D):** Test savollarini yechadi, to'g'ri variantni belgilaydi va yakunda qisqa test kalitlari xulosasini beradi:
  `1-savol — B ✅  2-savol — A ✅  3-savol — D ✅`
- **Rasmli savollar (OCR):** Kitob, daftar yoki test varaqasidan olingan sifatli rasmlarni o'qiydi va rasmdagi savollarni yechib beradi.
- **Noaniqlik nazorati:** Agar savol chala bo'lsa yoki kontekst yetishmasa, taxminiy javob bermay, aynan nima noaniq ekanligini bildiradi.
- **Anti-Flood (Spamdan himoya):** Bot serveriga ortiqcha yuk tushmasligi uchun so'rovlar oralig'i nazorat qilinadi.

---

## 📁 Loyiha Strukturasi

```text
BOT/
├── bot.py                  # Botni ishga tushiruvchi asosiy fayl
├── requirements.txt        # Kerakli kutubxonalar
├── .env                    # Bot sozlamalari
├── .env.example            # Sozlamalar namunasi
├── run.bat                 # Botni bitta bosishda ishga tushirish
├── install.bat             # Kutubxonalarni bitta bosishda o'rnatish
│
└── app/
    ├── core/               # Konfiguratsiya, logger va AI ko'rsatmalari
    ├── services/           # Kalitsiz bepul AI xizmati
    ├── handlers/           # Telegram xabarlarini qayta ishlovchi modullar
    ├── keyboards/          # Tugmalar va menyular
    ├── middlewares/        # Anti-flood va logging qatlamlari
    └── utils/              # Matnni formatlash va uzun xabarlarni bo'lish
```

---

## 🚀 Ishga Tushirish

Bot tokeni loyihaga to'liq kiritilgan:
`BOT_TOKEN=9243857438:AAG6I6TWcrd2D82wSZ3BtFxV0ff6qln-Ii0`

Botni ishga tushirish uchun:
1. Loyiha papkasidagi **`run.bat`** faylini 2 marta bosing.
2. Yoki terminalda quyidagini yozing:
```bash
python bot.py
```

Telegramda botingizga kiring va **/start** tugmasini bosing! 🎉
