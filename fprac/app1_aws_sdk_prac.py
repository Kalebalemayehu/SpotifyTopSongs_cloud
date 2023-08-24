from flask import Flask, redirect

app1 = Flask(__name__)

@app1.route('/')
def index():
    return redirect("http://localhost:5001/app2")

if __name__ == '__main__':
    app1.run(debug=True, port=5000)
