from flask import Flask, redirect

app2 = Flask(__name__)

@app2.route('/app2')
def app2_index():
    return "Hello from App 2! <a href='http://localhost:5000'>Go back to App 1</a>"

if __name__ == '__main__':
    app2.run(debug=True, port=5001)
