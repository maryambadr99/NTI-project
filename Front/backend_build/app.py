"""
Nile Skies — Backend API
يقرا ويكتب فعليًا في نفس ملفات الـ CSV بتاعة المشروع (مجلد data/).
شغّله بـ: python app.py  ثم افتح المتصفح على http://localhost:5000
"""
import csv
import os
from datetime import datetime

import pandas as pd
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

AIRCRAFT_CSV = os.path.join(DATA_DIR, "aircraft.csv")
FLIGHTS_CSV = os.path.join(DATA_DIR, "flights.csv")
HANGARS_CSV = os.path.join(DATA_DIR, "hangers.csv")
LABORS_CSV = os.path.join(DATA_DIR, "labors.csv")
ADMINS_CSV = os.path.join(DATA_DIR, "admins_pass.csv")
RESERVATIONS_CSV = os.path.join(DATA_DIR, "reservations.csv")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def read_csv_records(path):
    df = pd.read_csv(path, dtype=str).fillna("")
    return df.to_dict(orient="records")


def ensure_reservations_file():
    if not os.path.exists(RESERVATIONS_CSV):
        with open(RESERVATIONS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["reservation_id", "name", "phone", "email", "flight_id", "seats", "booked_at"]
            )


# ---------------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Read-only data endpoints
# ---------------------------------------------------------------------------
@app.route("/api/aircraft")
def get_aircraft():
    return jsonify(read_csv_records(AIRCRAFT_CSV))


@app.route("/api/flights")
def get_flights():
    return jsonify(read_csv_records(FLIGHTS_CSV))


@app.route("/api/hangars")
def get_hangars():
    return jsonify(read_csv_records(HANGARS_CSV))


@app.route("/api/labors")
def get_labors():
    return jsonify(read_csv_records(LABORS_CSV))


# ---------------------------------------------------------------------------
# Reservations — actually decrements available_seats in flights.csv
# and appends a row to reservations.csv
# ---------------------------------------------------------------------------
@app.route("/api/reservations", methods=["POST"])
def create_reservation():
    body = request.get_json(force=True) or {}
    name = (body.get("name") or "").strip()
    phone = (body.get("phone") or "").strip()
    email = (body.get("email") or "").strip()
    flight_id = str(body.get("flight_id") or "").strip()
    try:
        seats = int(body.get("seats"))
    except (TypeError, ValueError):
        return jsonify({"error": "عدد المقاعد غير صالح"}), 400

    if not name or not flight_id or seats <= 0:
        return jsonify({"error": "بيانات الحجز ناقصة"}), 400

    df = pd.read_csv(FLIGHTS_CSV, dtype=str)
    df["flight_id"] = df["flight_id"].astype(str)
    match = df[df["flight_id"] == flight_id]

    if match.empty:
        return jsonify({"error": "الرحلة غير موجودة"}), 404

    idx = match.index[0]
    available = int(df.at[idx, "available_seats"])

    if seats > available:
        return jsonify({"error": f"لا يوجد سوى {available} مقعد متاح على هذه الرحلة"}), 409

    # persist: decrement seats in flights.csv
    df.at[idx, "available_seats"] = str(available - seats)
    df.to_csv(FLIGHTS_CSV, index=False)

    # persist: append reservation record
    ensure_reservations_file()
    with open(RESERVATIONS_CSV, "r", encoding="utf-8") as f:
        reservation_id = sum(1 for _ in f)  # header + rows so far -> next id
    with open(RESERVATIONS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [reservation_id, name, phone, email, flight_id, seats,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        )

    flight = df.loc[idx].to_dict()
    return jsonify({
        "reservation_id": reservation_id,
        "name": name,
        "seats": seats,
        "flight": flight,
    }), 201


# ---------------------------------------------------------------------------
# Admin — login checked server-side against admins_pass.csv
# (the file itself is never sent to the browser)
# ---------------------------------------------------------------------------
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    body = request.get_json(force=True) or {}
    username = (body.get("username") or "").strip()
    password = (body.get("password") or "").strip()

    with open(ADMINS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 2 and row[0] == username and row[1] == password:
                return jsonify({"ok": True, "username": username})

    return jsonify({"ok": False, "error": "اسم المستخدم أو كلمة المرور غير صحيحة"}), 401


def check_admin(body):
    """Re-validates admin credentials on every write request (no sessions kept)."""
    username = (body.get("admin_username") or "").strip()
    password = (body.get("admin_password") or "").strip()
    with open(ADMINS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2 and row[0] == username and row[1] == password:
                return True
    return False


# ---------------------------------------------------------------------------
# Admin write endpoints — mirror admin.py's "Manage Aircrafts" / hangars
# ---------------------------------------------------------------------------
@app.route("/api/aircraft/<serial_number>", methods=["PATCH"])
def update_aircraft(serial_number):
    body = request.get_json(force=True) or {}
    if not check_admin(body):
        return jsonify({"error": "غير مصرح — بيانات دخول الأدمن غير صحيحة"}), 403

    new_status = body.get("status")
    valid = {"Active", "Maintenance", "Grounded", "Standby", "Available"}
    if new_status not in valid:
        return jsonify({"error": "حالة غير صالحة"}), 400

    df = pd.read_csv(AIRCRAFT_CSV, dtype=str)
    match = df[df["serial_number"] == serial_number]
    if match.empty:
        return jsonify({"error": "الطائرة غير موجودة"}), 404

    idx = match.index[0]
    df.at[idx, "status"] = new_status
    df.to_csv(AIRCRAFT_CSV, index=False)

    return jsonify(df.loc[idx].to_dict())


@app.route("/api/hangars/<hanger_id>", methods=["PATCH"])
def update_hangar(hanger_id):
    body = request.get_json(force=True) or {}
    if not check_admin(body):
        return jsonify({"error": "غير مصرح — بيانات دخول الأدمن غير صحيحة"}), 403

    new_status = body.get("status")
    if new_status not in {"Occupied", "Empty"}:
        return jsonify({"error": "حالة غير صالحة"}), 400

    df = pd.read_csv(HANGARS_CSV, dtype=str)
    match = df[df["Hanger"] == hanger_id]
    if match.empty:
        return jsonify({"error": "الحظيرة غير موجودة"}), 404

    idx = match.index[0]
    df.at[idx, "Status"] = new_status
    df.to_csv(HANGARS_CSV, index=False)

    return jsonify(df.loc[idx].to_dict())


if __name__ == "__main__":
    ensure_reservations_file()
    app.run(debug=True, port=5000)
