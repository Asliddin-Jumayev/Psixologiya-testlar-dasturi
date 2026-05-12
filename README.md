# Psixologiya-testlar-dasturi
Bunda 12 ta mavzu va har birida 20 tadan test bor o`qituvchi va talaba bo`lib kirish imkoniyati bor bazaga ulangan onlain 
🎓 AI Pedagog Monitoring Pro (v2.0.1)
Ushbu loyiha o'qituvchilar va talabalar o'rtasidagi bilimni baholash jarayonini avtomatlashtirish, test natijalarini real vaqt rejimida monitoring qilish va ma'lumotlarni bulutli texnologiyalar (Google Sheets) hamda Telegram orqali boshqarish uchun mo'ljallangan aqlli tizimdir.

🌟 Asosiy Imkoniyatlar
👨‍🎓 Talabalar uchun:
Mavzulashtirilgan Testlar: Google Sheets bazasidan olingan mavzular bo'yicha saralangan savollar.

Vaqt Nazorati: Har bir test uchun avtomatik taymer (10 daqiqa).

Interaktiv Dizayn: Zamonaviy va foydalanuvchiga qulay interfeys (customtkinter).

Tezkor Natija: Test yakunlanishi bilan ball va foiz ko'rsatkichini ko'rish.

👨‍🏫 O'qituvchilar (Admin) uchun:
Boshqaruv Paneli: Natijalarni ko'rish, savollarni tahrirlash va tizim sozlamalari.

Bulutli Baza: Savollar bazasini to'g'ridan-to'g'ri Google Sheets orqali yangilash imkoniyati.

Telegram Integratsiyasi: Har bir talaba testni tugatganda, natijalar o'qituvchining Telegram botiga xabar bo'lib boradi.

Natijalar Arxivi: SQLite mahalliy bazasida va Google Sheets bulutli bazasida natijalarni saqlash.

🛠️ Texnologik Stek
GUI: customtkinter (Zamonaviy Dark/Light UI).

Database: sqlite3 (Mahalliy) va Google Sheets API (Bulutli).

Integratsiya: Telegram Bot API (Bildirishnomalar uchun).

Til: Python 3.x.

🚀 O'rnatish va Ishga Tushirish
Kutubxonalarni o'rnating:

Bash
pip install customtkinter gspread oauth2client requests
Konfiguratsiya:

credentials.json faylini loyiha papkasiga joylang (Google Cloud Console'dan olingan).

Koddagi TOKEN va CHAT_ID o'zgaruvchilariga Telegram botingiz ma'lumotlarini kiriting.

Dasturni ishga tushiring:

Bash
python Main_App.py
📁 Loyiha Tuzilishi
Main_App.py — Dasturning asosiy kodi va mantiqiy qismi.

quiz_results.db — Natijalar saqlanadigan mahalliy ma'lumotlar bazasi.

credentials.json — Google API bilan bog'lanish uchun xavfsizlik kaliti.

📊 Tizim Arxitekturasi
Tizim quyidagi bosqichlarda ishlaydi:

Yuklash: Google Sheets'dan savollar bazasi yuklanadi.

Identifikatsiya: Foydalanuvchi talaba yoki o'qituvchi sifatida kiradi.

Testlash: Tasodifiy tanlangan savollar asosida test o'tkaziladi.

Sinxronizatsiya: Natijalar SQLite, Google Sheets va Telegramga yuboriladi.

👨‍💻 Muallif
Asliddin Jumayev — TATU Farg'ona filiali talabasi.
Loyiha bo'yicha savollar uchun: @Jumayev_Asliddin

⚠️ Eslatma
Dasturning to'liq ishlashi uchun Google Sheets'da Pedagog_Baza, AdminConfig va Natijalar nomli jadvallar mavjud bo'lishi shart.
