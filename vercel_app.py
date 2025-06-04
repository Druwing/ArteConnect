from app import create_app
from flask import Flask

app = create_app()

def handler(request):
    with app.app_context():
        response = app.full_dispatch_request()()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data().decode('utf-8')
        }