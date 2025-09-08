from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return 'hello flask world'

@app.route('/hi/<name>')
def hi(name):
    return f"hi world{name}"

@app.route('/hello/<name>')
def hello(name):
    return f"hello hahaha {name}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=31337)

