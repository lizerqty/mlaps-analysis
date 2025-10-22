"""
Simple HTTP server to run the MLAPS Dashboard
Usage: python run_dashboard.py
Then open: http://localhost:8000/mlaps_dashboard.html
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def find_free_port(start_port=8000):
    """Find a free port starting from start_port"""
    import socket
    port = start_port
    while port < start_port + 100:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    return None

def main():
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Find free port
    port = find_free_port(PORT)
    if not port:
        print("❌ Could not find a free port!")
        return
    
    print("=" * 70)
    print("🏠 MLAPS v2 Dashboard Server")
    print("=" * 70)
    print(f"\n✓ Server starting on http://localhost:{port}")
    print(f"\n📊 Dashboard URL: http://localhost:{port}/mlaps_dashboard.html")
    print(f"\n📁 Files available:")
    print(f"   - mlaps_dashboard.html (Interactive Dashboard)")
    print(f"   - mlaps_scores_v2.csv (Latest Results)")
    print(f"   - mlaps_analysis_v2.py (Analysis Code)")
    print("\n⌨️  Press Ctrl+C to stop the server")
    print("=" * 70)
    
    # Try to open browser automatically
    try:
        webbrowser.open(f'http://localhost:{port}/mlaps_dashboard.html')
        print("\n🌐 Opening dashboard in your browser...")
    except:
        print("\n💡 Please open the URL manually in your browser")
    
    # Start server
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()

