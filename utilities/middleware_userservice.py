from werkzeug.wrappers import Request, Response
from utilities.authentication import decode_token


class middleware():

    def __init__(self, app):
        self.app = app
        self.admin = {'Tao': "cool"}

    def __call__(self, environ, start_response):
        request = Request(environ)
        headers = dict(request.headers)
        authorization = headers['Authorization']
        token = authorization.split(' ')[-1]
        decoded = decode_token(token)
        username = decoded["userName"]
        password = decoded["passWord"]

        if username in self.admin.keys():
            if password == self.admin[username]:
                environ['user'] = {'name': username}
                return self.app(environ, start_response)
            else:
                res = Response('Unauthorized', mimetype='text/plain', status=401)
                return res(environ, start_response)
        else:
            res = Response('Forbidden', mimetype='text/plain', status=403)
            return res(environ, start_response)
