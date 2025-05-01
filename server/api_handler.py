from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import uuid

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import proebatb

SESSIONS = {}

class APIHandler(BaseHTTPRequestHandler):

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def parse_get_params(self):

        query = urlparse(self.path).query
        return parse_qs(query)

    def do_GET(self):
        params = self.parse_get_params()
        path = urlparse(self.path).path
        choice = None
        session_id = None
        if 'choice' in params:
            choice = params['choice'][0]
        if 'sessionId' in params:
            session_id = params['sessionId'][0]
        else:
            session_id = self.headers.get('X-Session-ID') or str(uuid.uuid4())
        if session_id not in SESSIONS:
            SESSIONS[session_id] = {'game': None, 'stage': None}

        state = SESSIONS[session_id]
        # Определяем путь запроса
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            game, message, needChoice = 0, "", False
            if state['game'] is None:
                game, message, needChoice = proebatb.choosingGame(choice)
            elif state['stage'] is None:
                game, message, needChoice = state['game'](choice)
            else:
                game, message, needChoice = state['stage'](choice)
            if type(game) is int:
                if state['stage'] is None:
                    self.connection.close()
                else:
                    state['stage'] = None
            else:
                if state['game'] is None:
                    state['game'] = game
                else:
                    state['stage'] = game
            response = {
                "message": message,
                "sessionId": session_id,
                "needChoice": needChoice,
                "status": "success"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            response = {
                "error": "Not Found",
                "status": "fail"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._send_response(200, {
            "message": "однажды вашу игру можно будет сохранить...",
            "received": json.loads(post_data),
            "status": "success"
        })