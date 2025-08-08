# Recircle

Recircle is a community-driven web platform built to encourage responsible sharing and reduce unnecessary waste. It empowers individuals to give or receive usable items while earning or spending points — building a sustainable loop of kindness in society.

---

## ✨ Philosophy

Recircle is not just a platform — it’s a mindset.

We believe that **every user is equal**, whether they’re giving, receiving, or doing both. There are no premium badges, no donor tags, and no receiver limits. Everyone participates as a **Kindler** — someone who lights a spark of change in the community.

The experience is built around a spark-based metaphor:

- **Kindler**: Every user is a kindler — they have the power to start change.
- **Send a Spark**: When a user gives something, they’re sending a spark — an act of kindness and generosity.
- **Catch a Spark**: When a user receives something, they’re catching that spark — continuing the chain of reuse and compassion.

There is no hierarchy, no judgment — only shared purpose. The goal is to give people a different kind of interaction: empowering, respectful, and beautifully human.

---

## 🌍 What It Does

- Let users **give away** items they no longer need.
- Let others **request and receive** those items.
- **Points system** rewards fair giving and respectful usage.
- No admin dashboard — fully user-controlled.
- Minimalistic, modern, and community-centered.

---

## 🔧 Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, Jinja2 templates
- **Database**: SQLite
- **Security**: Sessions, hashed passwords
- **Uploads**: Image storage via `/uploads`

---

## 💡 Key Features

- Item sharing with images and notes
- Accept and manage incoming requests
- Give and receive items fairly
- Earn and spend points automatically
- Lightweight and scalable structure

---

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/recircle.git
cd recircle
pip install flask werkzeug
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## 📁 Folder Structure

```
recircle/
│
├── static/
│   └── uploads/           # User-uploaded images
├── templates/             # HTML pages (give, receive, profile, etc.)
├── app.py                 # Main application logic
├── init_db.py             # Creates and seeds the database
└── database.db            # Auto-generated on first run
```

---

## 👨‍💻 Author

**Tahsin Hasan Shan**  
GitHub: [@tahsinshan](https://github.com/tahsinshan)

---

## 🛡 License

This project is open-source and available for community or educational use.