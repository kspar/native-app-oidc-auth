from flask import Flask, send_from_directory, request, Response, render_template
import conf
import socket
import threading
import webbrowser


app = Flask(__name__)


@app.route('/keycloak.json')
def keycloak_conf():
    return send_from_directory(".", "keycloak.json")


@app.route('/login')
def login():
    return render_template("login.html", idp_url=conf.IDP_URL, port=5000)


@app.route('/deliver-tokens', methods=['POST'])
def deliver_tokens():
    if request.is_json:
        body = request.get_json()
        print(body['access_token'])
        print(body['refresh_token'])

        return Response(status=200)

    else:
        return Response(status=400)


def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port



if __name__ == '__main__':
    port = get_free_port()
    print(port)

    url = 'http://127.0.0.1:{}/login'.format(port)
    threading.Timer(2, lambda: webbrowser.open(url)).start()

    app.run(host='127.0.0.1', port=port)
