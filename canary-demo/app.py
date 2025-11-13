from flask import Flask, Response
import os
import random

app = Flask(__name__)

# Read VERSION from environment variable, with proper fallback
VERSION = os.environ.get('VERSION', 'v1')
print(f"Starting app with VERSION: {VERSION}")  # Debug print

# Simple metrics
request_count = 0
error_count = 0

@app.route('/')
def hello():
    global request_count
    request_count += 1
    
    # Simulate occasional errors in v3 (10% error rate)
    if VERSION == 'v3' and random.random() < 0.1:
        global error_count
        error_count += 1
        return "Error!", 500
    
    # Different colors for each version
    if VERSION == 'v1':
        gradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    elif VERSION == 'v2':
        gradient = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
    elif VERSION == 'v3':
        gradient = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    else:
        gradient = 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
    
    return f'''
    <html>
        <head>
            <title>Canary Demo - {VERSION}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: {gradient};
                }}
                .container {{
                    text-align: center;
                    background: white;
                    padding: 50px;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                }}
                h1 {{
                    color: #333;
                    font-size: 3em;
                    margin: 0;
                }}
                .version {{
                    color: #e74c3c;
                    font-size: 2em;
                    margin-top: 20px;
                    font-weight: bold;
                }}
                .metrics {{
                    font-size: 1em;
                    color: #7f8c8d;
                    margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Canary Deployment Demo</h1>
                <p class="version">Version: {VERSION}</p>
                <p class="metrics">Requests: {request_count} | Errors: {error_count}</p>
            </div>
        </body>
    </html>
    '''

@app.route('/metrics')
def metrics():
    error_rate = (error_count / request_count * 100) if request_count > 0 else 0
    return Response(f'''# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{{app="canary-demo",version="{VERSION}"}} {request_count}

# HELP http_errors_total Total HTTP errors
# TYPE http_errors_total counter
http_errors_total{{app="canary-demo",version="{VERSION}"}} {error_count}

# HELP http_error_rate_percent HTTP error rate percentage
# TYPE http_error_rate_percent gauge
http_error_rate_percent{{app="canary-demo",version="{VERSION}"}} {error_rate}
''', mimetype='text/plain')

@app.route('/health')
def health():
    return {'status': 'healthy', 'version': VERSION}

if __name__ == '__main__':
    print(f"Application starting with VERSION={VERSION}")
    app.run(host='0.0.0.0', port=8080)