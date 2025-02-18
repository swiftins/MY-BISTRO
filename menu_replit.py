from flask import Flask, render_template

app = Flask(__name__)

menu_items = [
    {"id": 1, "title": "LANCH BOX N 1", "price": .99960},
    {"id": 2, "title": "LANCH BOX N 2", "price": 6.20},
    {"id": 3, "title": "LANCH BOX N 3", "price": 5.60},
     {"id": 4, "title": "LANCH BOX N 4", "price": 6.90}
]

@app.route("/")
def index():
    return render_template("index.html", menu_items=menu_items)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


