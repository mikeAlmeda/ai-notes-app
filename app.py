from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy", "message": "Flask app is running!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0") 