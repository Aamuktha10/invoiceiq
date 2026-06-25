import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

def get_orchestrator():
    from agents.orchestrator import OrchestratorAgent
    return OrchestratorAgent()

orchestrator = None

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/process-invoice", methods=["POST"])
def process_invoice():
    global orchestrator
    if orchestrator is None:
        orchestrator = get_orchestrator()
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    budget_limit = float(request.form.get("budget_limit", 50000))
    department = request.form.get("department", "General")
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    filename = secure_filename(file.filename)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    try:
        result = orchestrator.run(filepath=filepath, budget_limit=budget_limit, department=department)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route("/api/reports", methods=["GET"])
def get_reports():
    global orchestrator
    if orchestrator is None:
        return jsonify([])
    return jsonify(orchestrator.get_report_log())

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True, port=5000)