from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os
import subprocess
import sys
from datetime import datetime
import string
import random

MAX_COMMAND_WAIT_TIME = 10

def generateRandomString(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def log(message):
    print(f"[{datetime.now().isoformat()}]: {message}", file=sys.stderr)

def fail(message):
    log(message)
    sys.exit(1)

def run(command):
    log(f"Running {' '.join(command)}")
    try:
        subprocess.run(
            command,
            timeout=MAX_COMMAND_WAIT_TIME,
            check=True,
            stderr=sys.stderr,
            stdout=sys.stderr
        )
    except subprocess.TimeoutExpired:
        fail(f"Command timed out: {' '.join(command)}")
    except subprocess.CalledProcessError:
        fail(f"{command[0]} invocation failed")
    print(file=sys.stderr)

def output_file(filename):
    ## get file and return contents from function
    out = ""
    with open(filename, 'r') as f:
        out = f.read()
    return out

def process_latex(latex):
    os.chdir('/tmp')

    random_suffix = generateRandomString(8)

    # Read LaTeX content from stdin
    with open(f'render{random_suffix}.tex', 'wb') as f:
        f.write(latex)

    # Run commands
    run(['latex', '-halt-on-error', '-interaction=nonstopmode', '-no-shell-escape', f'/tmp/render{random_suffix}.tex'])
    run(['dvisvgm', '--no-fonts', '--verbosity=1', f'/tmp/render{random_suffix}.dvi', '--exact', f'--output=/tmp/render{random_suffix}.svg'])
    run(['rsvg-convert', '-o', f'render{random_suffix}.png', f'/tmp/render{random_suffix}.svg'])

    # Validate PNG
    if not os.path.isfile(f'render{random_suffix}.png'):
        fail('PNG was not generated')
    
    png_size = os.path.getsize(f'render{random_suffix}.png')
    if png_size < 24:
        fail('PNG file too small')
    
    with open(f'render{random_suffix}.png', 'rb') as f:
        magic = f.read(4)
        if magic != b'\x89PNG':
            fail('no PNG magic number found')
        f.seek(12)
        ihdr = f.read(4)
        if ihdr != b'IHDR':
            fail('no IHDR in PNG')

    # Output PNG dimensions (width and height)
    with open(f'render{random_suffix}.png', 'rb') as f:
        f.seek(16)
        dimensions = f.read(8)
        sys.stdout.buffer.write(dimensions)

    # return contents of svg file
    svgcontents = output_file(f'render{random_suffix}.svg')
    # Clean up
    os.remove(f'render{random_suffix}.tex')
    os.remove(f'render{random_suffix}.dvi')
    os.remove(f'render{random_suffix}.png')
    os.remove(f'render{random_suffix}.svg')
    
    return svgcontents

app = Flask(__name__)
CORS(app)

## basic flask app
@app.route('/generate', methods=['POST'])
def convert():
    latex_input = request.data
    output = process_latex(latex_input)
    return jsonify({'svg': output})


@app.route("/")
def index():
    return Response("Welcome to the LaTeX to SVG converter!", mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
