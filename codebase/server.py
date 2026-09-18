"""Local-only demo server. Run: python -m codebase.server"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from .agent import classify_context, get_config

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Student messages must not leak to terminal access logs.

    def send(self, status, body, content_type='application/json; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/':
            self.send(200, Path(__file__).with_name('index.html').read_bytes(), 'text/html; charset=utf-8')
        elif self.path == '/health':
            config = get_config()
            self.send(200, json.dumps({'configured': bool(config['api_key']),
                                      'provider': config['provider'], 'key_name': config['key_name'],
                                      'model': config['model']}).encode())
        else:
            self.send(404, b'{}')

    def do_POST(self):
        if self.path != '/api/classify':
            return self.send(404, b'{}')
        if self.headers.get('Origin') not in (None, 'http://127.0.0.1:8765', 'http://localhost:8765'):
            return self.send(403, b'{"error":"origin_denied"}')
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 70000:
                raise ValueError('invalid_body_size')
            if 'application/json' not in self.headers.get('Content-Type', ''):
                raise ValueError('json_required')
            body = json.loads(self.rfile.read(size))
            result = classify_context(body.get('message'), body.get('attachments', []))
            self.send(200, json.dumps(result, ensure_ascii=False).encode())
        except (ValueError, AttributeError):
            self.send(400, b'{"error":"invalid_input"}')


if __name__ == '__main__':
    print('Discord TA prototype: http://127.0.0.1:8765', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
