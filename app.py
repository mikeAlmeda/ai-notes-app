from flask import Flask, render_template, jsonify, request
from models import db, Note
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created!")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy", "message": "Flask app is running!"})

@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content are required."}), 400   #bad
    note = Note(title=data["title"], content=data["content"])
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201  #created

@app.route("/api/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes])
    
@app.route("/api/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]
    db.session.commit()
    return jsonify(note.to_dict()), 200

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully"}), 204

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0") 