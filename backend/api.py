from flask import Flask, jsonify, request
from aml_trigger import submit_pipeline_job
from storage import upload_bytes

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/upload-trigger")
def upload_trigger():
    if "file" not in request.files:
        return jsonify({"error": "file is required"}), 400

    uploaded = request.files["file"]
    if uploaded.filename == "":
        return jsonify({"error": "file name is empty"}), 400

    blob_url = upload_bytes(uploaded.filename, uploaded.read())
    job_name, studio_url = submit_pipeline_job(blob_url)

    return (
        jsonify(
            {
                "status": "submitted",
                "blob_url": blob_url,
                "job_name": job_name,
                "ml_studio_job_url": studio_url,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
