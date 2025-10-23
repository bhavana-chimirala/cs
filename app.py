from flask import Flask, request, make_response
import re
import os

app = Flask(__name__, static_folder='.', template_folder='.')

# Simple practical regex for syntax check
SYNTAX_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_syntax(email: str) -> bool:
    return bool(SYNTAX_RE.match(email.strip()))

@app.route('/')
def index():
    # Serve index.html directly from file (static)
    return app.send_static_file('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    email = request.form.get('email', '').strip()
    if not email:
        ok = False
        reason = 'empty'
    else:
        ok = is_valid_syntax(email)
        reason = 'syntax_ok' if ok else 'invalid_syntax'

    # Load result.html, replace placeholders (very small templating)
    with open('result.html', 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('{{EMAIL}}', email)
    html = html.replace('{{OK}}', 'true' if ok else 'false')
    html = html.replace('{{REASON}}', reason)
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting app on 0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)
