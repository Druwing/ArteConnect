from app import create_app
from flask import Response
import os

app = create_app()

def wsgi_app(environ, start_response):
    with app.request_context(environ):
        try:
            response = app.full_dispatch_request()
        except Exception as e:
            response = app.make_response(str(e))
            response.status_code = 500
        
        start_response(f"{response.status_code} {response.status}",list(response.headers.items()))
        
        return [response.get_data()]

def handler(event, context):
    """Handler principal para o Vercel"""
    from werkzeug.wrappers import Request
    from werkzeug.datastructures import Headers
    
    # Converte o evento do Vercel para ambiente WSGI
    headers = Headers()
    for key, value in (event.get('headers') or {}).items():
        headers.add(key, value)
    
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', {}),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'wsgi.url_scheme': headers.get('X-Forwarded-Proto', 'https'),
        'wsgi.input': event.get('body', ''),
        'wsgi.errors': None,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        **{'HTTP_' + k.upper().replace('-', '_'): v for k, v in headers.items()}
    }
    
    # Processa a requisição
    response_data = []
    
    def start_response(status, response_headers):
        nonlocal response_data
        response_data[:] = [status, response_headers]
    
    body = b''.join(wsgi_app(environ, start_response))
    
    status_code = int(response_data[0].split()[0])
    headers = dict(response_data[1])
    
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': body.decode('utf-8')
    }
