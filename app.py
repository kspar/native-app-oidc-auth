from flask import Flask, send_from_directory, request, Response, render_template

app = Flask(__name__)


@app.route('/keycloak.json')
def keycloak_conf():
    return send_from_directory(".", "keycloak.json")


@app.route('/login')
def login():
    return render_template("login.html", a=1, b=3)


@app.route('/deliver-tokens', methods=['POST'])
def deliver_tokens():
    if request.is_json:
        body = request.get_json()
        print(body['access_token'])
        print(body['refresh_token'])

        return Response(status=200)

    else:
        return Response(status=400)


if __name__ == '__main__':
    app.run()
