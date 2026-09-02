from datetime import datetime, timezone
import os
import sqlite3

from flask import Flask, jsonify, request
from waitress import serve

app = Flask(__name__)
DATABASE_PATH = os.environ.get("TRANSPILATRON_TELEMETRY_DB", "pings.db")


def initialize_database() -> None:
	with sqlite3.connect(DATABASE_PATH) as database:
		database.execute(
			"""
			CREATE TABLE IF NOT EXISTS pings (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				event_type TEXT NOT NULL,
				version TEXT NOT NULL,
				received_at TEXT NOT NULL
			)
			"""
		)


@app.post("/ping")
def ping():
	payload = request.get_json(silent=True)
	if not isinstance(payload, dict):
		return jsonify(error="Request body must be a JSON object"), 400

	event_type = payload.get("type")
	version = payload.get("version")
	if not isinstance(event_type, str) or not event_type.strip():
		return jsonify(error="'type' must be a non-empty string"), 400
	if not isinstance(version, str) or not version.strip():
		return jsonify(error="'version' must be a non-empty string"), 400

	with sqlite3.connect(DATABASE_PATH) as database:
		database.execute(
			"INSERT INTO pings (event_type, version, received_at) VALUES (?, ?, ?)",
			(event_type, version, datetime.now(timezone.utc).isoformat()),
		)

	return jsonify(status="ok"), 201


@app.get("/health")
def health():
	return jsonify(status="ok")


initialize_database()


if __name__ == "__main__":
	serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))