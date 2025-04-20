from app import create_app, socketio

FlaskApp = create_app()

if __name__ == '__main__':
    socketio.run(FlaskApp, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)