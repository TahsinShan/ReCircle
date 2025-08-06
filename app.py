from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'super-secret-key'


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            points INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            location TEXT,
            item TEXT,
            expiry TEXT,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            receiver_id INTEGER,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (item_id) REFERENCES items(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/points')
def points():
    return render_template('points.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            return "Passwords do not match", 400

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                      (name, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Email already registered", 400

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT id, name, password FROM users WHERE email = ?', (email,))
        user = c.fetchone()

        # Check for any accepted applications before clearing DB
        accepted_item_id = None
        if user:
            c.execute('''
                SELECT item_id FROM applications
                WHERE receiver_id = ? AND status = 'accepted'
                ORDER BY id DESC LIMIT 1
            ''', (user[0],))
            accepted = c.fetchone()
            if accepted:
                accepted_item_id = accepted[0]

        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            if accepted_item_id:
                session['accepted_item_id'] = accepted_item_id
            return redirect('/')
        else:
            return "Invalid email or password", 401

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/give', methods=['GET', 'POST'])
def give():
    if not session.get('user_id'):
        return redirect('/login')

    if request.method == 'POST':
        user_id = session.get('user_id')
        name = session.get('user_name')
        location = request.form['location']
        item = request.form['item']
        expiry = request.form.get('expiry', '')
        notes = request.form.get('notes', '')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO items (user_id, name, location, item, expiry, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, name, location, item, expiry, notes))

        c.execute('UPDATE users SET points = points + 5 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

        return redirect('/thanks')

    return render_template('give.html')


@app.route('/receive')
def receive():
    if not session.get('user_id'):
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, item, location, notes, user_id FROM items')
    rows = c.fetchall()
    conn.close()

    items = [
        {'id': row[0], 'item': row[1], 'location': row[2], 'notes': row[3], 'user_id': row[4]}
        for row in rows
    ]
    return render_template('receive.html', items=items)


@app.route('/apply/<int:item_id>', methods=['POST'])
def apply(item_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM applications WHERE item_id = ? AND receiver_id = ?', (item_id, user_id))
    existing = c.fetchone()

    if not existing:
        c.execute('INSERT INTO applications (item_id, receiver_id) VALUES (?, ?)', (item_id, user_id))
        conn.commit()

    conn.close()
    return redirect('/receive')


@app.route('/manage_requests/<int:item_id>', methods=['GET', 'POST'])
def manage_requests(item_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM items WHERE id = ?', (item_id,))
    owner = c.fetchone()
    if not owner or owner[0] != user_id:
        conn.close()
        return "Unauthorized", 403

    if request.method == 'POST':
        action = request.form['action']
        receiver_id = int(request.form['receiver_id'])

        if action == 'accept':
            c.execute('''
                UPDATE applications SET status = 'accepted'
                WHERE item_id = ? AND receiver_id = ?
            ''', (item_id, receiver_id))

            c.execute('''
                UPDATE applications SET status = 'declined'
                WHERE item_id = ? AND receiver_id != ?
            ''', (item_id, receiver_id))

            c.execute('DELETE FROM items WHERE id = ?', (item_id,))

        elif action == 'decline':
            c.execute('''
                UPDATE applications SET status = 'declined'
                WHERE item_id = ? AND receiver_id = ?
            ''', (item_id, receiver_id))

        conn.commit()

    c.execute('''
        SELECT applications.receiver_id, users.name, applications.status
        FROM applications
        JOIN users ON users.id = applications.receiver_id
        WHERE applications.item_id = ?
    ''', (item_id,))
    applications = c.fetchall()
    conn.close()

    return render_template('manage_requests.html', applications=applications, item_id=item_id)


@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check for new accepted applications
    c.execute('''
        SELECT item_id FROM applications
        WHERE receiver_id = ? AND status = 'accepted'
        ORDER BY id DESC LIMIT 1
    ''', (user_id,))
    accepted = c.fetchone()

    accepted_item_id = None
    if accepted:
        accepted_item_id = accepted[0]

    # Load user and posts
    c.execute('SELECT name, email, points FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    c.execute('SELECT id, item, location, expiry, notes FROM items WHERE user_id = ?', (user_id,))
    posts = c.fetchall()

    conn.close()

    return render_template('profile.html', user=user, posts=posts, accepted_item_id=accepted_item_id)


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM items WHERE id = ?', (item_id,))
    owner = c.fetchone()

    if owner and owner[0] == user_id:
        c.execute('DELETE FROM items WHERE id = ?', (item_id,))
        c.execute('''
            UPDATE users
            SET points = MAX(points - 5, 0)
            WHERE id = ?
        ''', (user_id,))
        conn.commit()

    conn.close()
    return redirect('/profile')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
