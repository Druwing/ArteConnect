from app import create_app
from flask import Response
import os

app = create_app()

def handler(event, context):
    """Handler para o ambiente serverless do Vercel"""
    from io import BytesIO
    from werkzeug.datastructures import Headers
    
    headers = Headers()
    for key, value in (event.get('headers') or {}).items():
        headers.add(key, value)
    
    body = event.get('body', '') or ''
    if isinstance(body, dict):
        import json
        body = json.dumps(body)
    
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in (event.get('queryStringParameters') or {}).items()]),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'wsgi.url_scheme': headers.get('X-Forwarded-Proto', 'https'),
        'wsgi.input': BytesIO(body.encode('utf-8')),
        'wsgi.errors': None,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        **{'HTTP_' + k.upper().replace('-', '_'): v for k, v in headers.items()}
    }
    
    response_headers = []
    response_body = []
    
    def start_response(status, headers, exc_info=None):
        nonlocal response_headers
        response_headers[:] = [status, headers]
        return response_body.append
    
    app_iter = app(environ, start_response)
    try:
        response_body.extend(iter(app_iter))
    finally:
        if hasattr(app_iter, 'close'):
            app_iter.close()
    
    status_code = int(response_headers[0].split()[0])
    headers_dict = dict(response_headers[1])
    
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': b''.join(response_body).decode('utf-8')
    }
