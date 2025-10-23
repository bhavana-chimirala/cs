from flask import Flask, request, render_template
import re
import os

app = Flask(__name__)

# Simple practical regex for syntax check
SYNTAX_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_syntax(email: str) -> bool:
    return bool(SYNTAX_RE.match(email.strip()))

@app.route('/')
def index():
    # Render the email input form
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    email = request.form.get('email', '').strip()
    if not email:
        ok = False
        reason = 'empty'
    else:
        ok = is_valid_syntax(email)
        reason = 'syntax_ok' if ok else 'invalid_syntax'

    # Render result page with template variables
    return render_template('result.html', EMAIL=email, OK=ok, REASON=reason)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting app on 0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)
