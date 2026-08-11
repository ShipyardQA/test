"""Tiny HTTP server so the environment deploys and the build-arg result is verifiable.

GET / returns the build-time facts baked at build time:
  - sha256 of the API_KEY build arg (proves the resolved Vault value reached the build)
  - its length

Never returns the raw secret. Verify on QA with a curl to the environment's URL, or:
  kubectl -n <ns> exec <pod> -- cat /build-info.txt
"""

from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('/build-info.txt') as f:
                body = f.read()
        except OSError:
            body = 'build-info missing\n'
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
