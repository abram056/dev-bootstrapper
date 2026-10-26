from {{package_name}}.app import app


def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"{{project_name}}" in response.data
