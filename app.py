from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')  # Set a strong secret key in production

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    with open("SCHOOL.txt", 'a') as z:
        z.write('NAME  :  ' + data['name'] + '\n\n')
        z.write('CLASS : ' + data['class'] + '\n\n')
        z.write('SECTION : ' + data['section'] + '\n\n')
        z.write('ADMITION NO. : ' + data['admission'] + '\n\n')
        z.write('MOBAIL NO. : ' + data['mobile'] + '\n\n')
        z.write('ADDRESS : ' + data['address'] + '\n\n')
        z.write("===================================================\n\n")
    return jsonify({"message": "Student data saved successfully!"})

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'sohaib12' and password == 'adminrashid':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = 'Invalid username or password.'
    return render_template('admin_login.html', error=error)

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    try:
        with open("SCHOOL.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        content = "No data available."
    return render_template("admin.html", content=content)

@app.route('/clear', methods=['POST'])
def clear_data():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    open("SCHOOL.txt", "w").close()
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/view')
def view_data():
    try:
        with open("SCHOOL.txt", "r") as file:
            content = file.read().replace('\n', '<br>')
        return f"<h2>Saved Student Data</h2><div>{content}</div>"
    except FileNotFoundError:
        return "No data found yet."

if __name__ == "__main__":
    app.run()
