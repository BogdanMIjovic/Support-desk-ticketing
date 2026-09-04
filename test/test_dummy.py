def test_dummy(client):
    response = client.get("/ticket")
    assert response.status_code == 401


