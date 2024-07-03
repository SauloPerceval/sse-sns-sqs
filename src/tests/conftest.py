import pytest


@pytest.fixture(scope="package")
def client():
    from app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    
    with app.app_context():
        yield client
