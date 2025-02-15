import os
import click
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from utilities.util import FilePath, is_moku_project_dir, write_error_msg

@click.command()
@click.option("--port", default=8000, help="Port to serve the site")
def serve(port):
    if not is_moku_project_dir():
        write_error_msg("not in a project directory")
        return 
    if not os.path.exists(FilePath.OUTPUT_DIR.cwd_path):
        write_error_msg("no output found. run 'build' first")
        return
    if not os.path.isdir(FilePath.OUTPUT_DIR.cwd_path):
        write_error_msg("no output found. run 'build' first")
        return
    
    webbrowser.open(f"http://localhost:{port}")
    serve_page(port)

def serve_page(port: int): 
    os.chdir(FilePath.OUTPUT_DIR.cwd_path)
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, SimpleHTTPRequestHandler)
    click.secho(f"Serving at http://localhost:{port}")
    httpd.serve_forever()
