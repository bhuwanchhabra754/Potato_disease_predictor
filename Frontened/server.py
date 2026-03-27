"""
Simple HTTP server to serve the frontend with CORS support.
Run this from the Frontened folder to serve index.html
"""

import http.server
import socketserver
import os
from urllib.parse import urlparse
from pathlib import Path

PORT = 3000
FRONTEND_DIR = Path(__file__).parent.absolute()


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS support"""

    def end_headers(self):
        """Add CORS headers to all responses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle OPTIONS requests"""
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """Serve files from frontend directory"""
        # Parse the URL
        parsed_path = urlparse(self.path).path
        
        # Default to index.html for root
        if parsed_path == '/':
            parsed_path = '/index.html'
        
        # Construct file path
        file_path = FRONTEND_DIR / parsed_path.lstrip('/')
        
        # Security: prevent directory traversal
        try:
            file_path = file_path.resolve()
            if not str(file_path).startswith(str(FRONTEND_DIR)):
                self.send_error(403, 'Access Denied')
                return
        except Exception:
            self.send_error(400, 'Bad Request')
            return
        
        # Serve the file if it exists
        if file_path.is_file():
            self.send_response(200)
            
            # Set appropriate Content-Type
            if file_path.suffix == '.html':
                self.send_header('Content-type', 'text/html; charset=utf-8')
            elif file_path.suffix == '.css':
                self.send_header('Content-type', 'text/css; charset=utf-8')
            elif file_path.suffix == '.js':
                self.send_header('Content-type', 'application/javascript; charset=utf-8')
            elif file_path.suffix in ['.png', '.jpg', '.jpeg', '.gif']:
                mime_type = 'image/' + file_path.suffix.lstrip('.')
                self.send_header('Content-type', mime_type)
            else:
                self.send_header('Content-type', 'application/octet-stream')
            
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Serve index.html for undefined routes (SPA support)
            index_path = FRONTEND_DIR / 'index.html'
            if index_path.exists():
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(index_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'File Not Found')


if __name__ == '__main__':
    os.chdir(FRONTEND_DIR)
    
    try:
        with socketserver.TCPServer(('', PORT), CORSRequestHandler) as httpd:
            print(f'')
            print(f'╔════════════════════════════════════════╗')
            print(f'║  Frontend Server Running               ║')
            print(f'║  🌐 http://localhost:{PORT}                 ║')
            print(f'║  📁 Serving: {str(FRONTEND_DIR)}')
            print(f'╚════════════════════════════════════════╝')
            print(f'')
            print(f'Press Ctrl+C to stop the server')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n\n✓ Server stopped')
    except OSError as e:
        if e.errno == 48:
            print(f'✗ Error: Port {PORT} is already in use')
            print(f'  Try killing the process using port {PORT}:')
            print(f'  netstat -ano | findstr :{PORT}')
            print(f'  taskkill /PID <PID> /F')
        else:
            print(f'✗ Error: {e}')
