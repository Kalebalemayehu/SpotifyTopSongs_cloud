from flask import Flask, request, redirect

app = Flask(__name__)

authorization_code = None

@app.route('/')
def index():
    return redirect("/callback")

@app.route('/callback')
def callback():
    global authorization_code
    authorization_code = request.args.get('code')
    return "Authentication successful! You can close this window."

if __name__ == '__main__':
    app.run(debug=True, port=5001)
