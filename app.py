from flask import Flask, render_template, request, jsonify

from chat import get_response

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.route("/Contact")
def Contact():
    return render_template("contact.html")

@app.route("/tenth")
def tenth():
    return render_template("10th.html")

@app.route("/twelve")
def twelve():
    return render_template("12th.html")

@app.route("/College")
def College():
    return render_template("college.html")

@app.route("/Suggestion")
def tips():
    return render_template("tips.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
