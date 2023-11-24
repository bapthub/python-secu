from flask import Flask,request,render_template,redirect,url_for, flash, send_file


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

### LOGIN PAGE
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

### SIGN-UP PAGE
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

### CODE VERIFICATION PAGE
@app.route('/code', methods=['GET'])
def code():
    return render_template('code.html')

### RESEND CODE PAGE
@app.route('/resend', methods=['GET'])
def resend():
    return render_template('resend.html')

### CERTIFICATE WITH AUTHENTICATION PAGE
@app.route('/certificate', methods=['GET'])
def certificate():
    return render_template('certificate.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
