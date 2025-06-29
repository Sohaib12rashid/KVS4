from flask import Flask, request, jsonify, render_template, redirect
app = Flask(__name__)

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

@app.route('/admin')
def admin_panel():
    try:
        with open("SCHOOL.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        content = "No data available."
    return render_template("admin.html", content=content)

@app.route('/clear', methods=['POST'])
def clear_data():
    open("SCHOOL.txt", "w").close()
    return redirect('/admin')

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
