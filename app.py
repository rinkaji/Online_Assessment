from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def old():
    return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template("login_page.html")
    
    if request.method == "POST":
        return "login"
    
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template('register_page.html')
    
    if request.method == "POST":
        return "Student success fully registered"

@app.route('/index')
def home():
    return render_template("show_classes_page.html")


if __name__ == "__main__":
    app.run(debug=True)