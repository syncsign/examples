# -*- coding: UTF-8 -*-
import logging
import uasyncio as asyncio
import ujson as json
from core.constants import *
import ubinascii
import picoweb

DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWD   = 'password'

log = logging.getLogger("APP")
logging.basicConfig(level=logging.INFO)

app = picoweb.WebApp(__name__)

HTML_TEMPLATE_HEADER = 'app/header.tpl'
HTML_TEMPLATE_FOOTER = 'app/footer.tpl'
HTML_TEMPLATE_INDEX_BODY = 'app/index.tpl'
HTML_TEMPLATE_ADMIN_BODY = 'app/admin.tpl'

def require_auth(func):
    def auth(req, resp):
        auth = req.headers.get(b"Authorization")
        if not auth:
            log.warning('no auth found')
            yield from resp.awrite(
                'HTTP/1.0 401 NA\r\n'
                'WWW-Authenticate: Basic realm="SyncSign Web Realm"\r\n'
                '\r\n'
            )
            return
        auth = auth.split(None, 1)[1]
        auth = ubinascii.a2b_base64(auth).decode()
        req.username, req.passwd = auth.split(":", 1)
        # verify credential
        try:
            if req.username == DEFAULT_USERNAME and req.passwd == DEFAULT_PASSWD:
                yield from func(req, resp)
            else:
                log.warning('not match')
                raise ValueError('Invalid configuration, or unauthorized access is prohibited.')
        except Exception as e: # if first run
            log.exception(e, 'error occured.')
            yield from picoweb.start_response(resp, content_type="text/html", status="401", headers=None) # 403 cannot continue with a bad password input
            yield from resp.awrite("Unauthorized access is prohibited.")

    return auth

def oops(resp):
    log.warning('oops')
    yield from picoweb.start_response(resp, content_type="text/html", status=500, headers=None)
    yield from resp.awrite("Oops.")

@app.route("/")
def index(req, resp):
    try:
        with open(HTML_TEMPLATE_HEADER,'r') as f:
            _header = f.read()
        with open(HTML_TEMPLATE_INDEX_BODY,'r') as f:
            _body = f.read()
        with open(HTML_TEMPLATE_FOOTER,'r') as f:
            _footer = f.read()
        yield from picoweb.start_response(resp, content_type="text/html", status=200, headers=None)
        yield from resp.awrite(_header)
        yield from resp.awrite(_body)
        yield from resp.awrite(_footer)
    except Exception as e:
        log.exception(e, '/admin')
        yield from oops(resp)

@app.route("/admin")
@require_auth
def admin(req, resp):
    try: # % (req.username)
        success = False
        if req.method == "POST":
            yield from req.read_form_data()
            passwd = req.form["passwd"]
            log.info('TODO: save password: %s', passwd)
            success = True
        else:  # GET
            passwd = DEFAULT_PASSWD
        with open(HTML_TEMPLATE_HEADER,'r') as f:
            _header = f.read()
        with open(HTML_TEMPLATE_ADMIN_BODY,'r') as f:
            _body = f.read()
        with open(HTML_TEMPLATE_FOOTER,'r') as f:
            _footer = f.read()
        yield from picoweb.start_response(resp, content_type="text/html; charset=UTF-8")
        yield from resp.awrite(_header)
        yield from resp.awrite(_body.format(passwd = passwd))
        if success:
            yield from resp.awrite('<div class="alert alert-success" role="alert">OK.</div>')
        yield from resp.awrite(_footer)
    except Exception as e:
        log.exception(e, '/admin')
        yield from oops(resp)

class App:

    def __init__(self, mgr, loop, pan):
        app.run(host="0.0.0.0", port=10000)
