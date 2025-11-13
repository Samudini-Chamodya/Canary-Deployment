from flask import Flask, Response
import os
import random
import time

app = Flask(__name__)
VERSION = os.getenv('VERSION', 'v3')

# Simple metrics
request_count = 0
error_count = 0

@app.route('/')
def hello():
    global request_count
    request_count += 1
    
    # Simulate occasional errors in v3 (10% error rate for testing)
    if VERSION == 'v3' and random.random() < 0.1:
        global error_count
        error_count += 1
        return "Error!", 500
    
    return f'''
    <html>
        <head>
            <title>Canary Demo</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if VERSION == 'v1' 
                                 else 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' if VERSION == 'v2'
                                 else 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'};
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
                p {{
                    color: #666;
                    font-size: 1.5em;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Canary Deployment Demo</h1>
                <p>You are seeing: <strong>{VERSION}</strong></p>
            </div>
        </body>
    </html>
    '''

@app.route('/metrics')
def metrics():
    error_rate = (error_count / request_count * 100) if request_count > 0 else 0
    return Response(f'''# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total {request_count}

# HELP http_errors_total Total HTTP errors
# TYPE http_errors_total counter
http_errors_total {error_count}

# HELP http_error_rate_percent HTTP error rate percentage
# TYPE http_error_rate_percent gauge
http_error_rate_percent {error_rate}
''', mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)