from app import create_app, socket

app = create_app(debug=True)

if __name__ == '__main__':
    print('running socketio server')
    socket.run(app, host='0.0.0.0')
