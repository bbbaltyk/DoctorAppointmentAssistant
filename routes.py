from flask import render_template, request, url_for, redirect, jsonify, Flask
from models import Slot
import sys
import subprocess
from app import socketio

bot_process = None

def register_routes(app, db):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            slots = Slot.query.all()
            return render_template('index.html', slots=slots)
        if request.method == 'POST':
            speciality = request.form.get("specialist").lower()
            name = request.form.get("name")
            date = request.form.get("date")
            open_slot = True if 'booked' in request.form.keys() else False

            slot = Slot(speciality = speciality, name=name, date=date, open_slot=open_slot)
            db.session.add(slot)
            db.session.commit()
            slots = Slot.query.all()

            return render_template('index.html', slots=slots)

    @app.route("/delete/<did>")
    def delete_slot(did):
        Slot.query.filter(Slot.did == did).delete()

        db.session.commit()
        slots = Slot.query.all()
        return render_template('index.html', slots=slots)

    @app.route("/start_voice_bot", methods=["POST"])
    def start_voice_bot():
        global bot_process
        socketio.emit('bot_status', {'status': 'starting'})
        if bot_process is None:
            bot_process = subprocess.Popen([sys.executable, "chatbot.py"])
            return jsonify({"status":"started"})
        return jsonify({"status": "already running"})

    @app.route("/stop_voice_bot", methods=["POST"])
    def stop_voice_bot():
        global bot_process
        socketio.emit('bot_status', {'status': 'stopping'})
        if bot_process is not None:
            bot_process.terminate()
            bot_process = None
            return jsonify({'status': 'stopped'})
        return jsonify({"status": "not running"})

    @app.route("/update_status", methods=["POST"])
    def update_status():
        data = request.get_json()
        status = data.get("status")

        socketio.emit("bot_status", {"status": status})
        return jsonify({"message": "status updated"}), 200