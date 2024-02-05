from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Halo, ini adalah halaman web sederhana menggunakan Flask!"

if __name__ == '__main__':
    app.run(debug=True)
