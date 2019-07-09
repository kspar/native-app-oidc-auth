from flask import Flask, send_from_directory, request, Response, render_template
import conf
import socket
import threading
import webbrowser
import subprocess

PORT_RANGE_FIRST = 5100
PORT_RANGE_LAST = 5109

app = Flask(__name__)

port = None
browser_process = None


@app.route('/keycloak.json')
def keycloak_conf():
    return send_from_directory(".", "keycloak.json")


@app.route('/login')
def login():
    return render_template("login.html", idp_url=conf.IDP_URL, port=port)


@app.route('/deliver-tokens', methods=['POST'])
def deliver_tokens():
    if request.is_json:
        body = request.get_json()
        print(body['access_token'])
        print(body['refresh_token'])

        if browser_process is not None:
            print("Terminating")
            browser_process.terminate()
        else:
            print("Browser process is None ???")

        return Response(status=200)

    else:
        return Response(status=400)


def get_free_port():
    for p in range(PORT_RANGE_FIRST, PORT_RANGE_LAST + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('127.0.0.1', p))
            sock.close()
            return p
        except OSError:
            # Port already in use?
            pass

    raise OSError("Unable to bind to ports {} - {}".format(PORT_RANGE_FIRST, PORT_RANGE_LAST))


def open_browser(url):
    global browser_process
    browser_name = webbrowser.get().name
    browser_process = subprocess.Popen([browser_name, url],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def start_auth():
    global port
    port = get_free_port()
    url = 'http://127.0.0.1:{}/login'.format(port)

    # Assume the server starts in 1 second
    threading.Timer(1, lambda: open_browser(url)).start()

    app.run(host='127.0.0.1', port=port)


if __name__ == '__main__':
    start_auth()
