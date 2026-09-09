def test_create_ticket(client):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234"}
    )

    response_for_token = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234"}
    )

    response_for_token_data = response_for_token.json()
    token = response_for_token_data["access_token"]

    response = client.post(
        "/ticket",
        json={"title": "First test",
              "description": "This is the first test",
              },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert "title" in data
    assert "description" in data

def test_list_own_tickets(client):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234"}
    )

    response_for_token = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234"}
    )

    response_for_token_data = response_for_token.json()
    token = response_for_token_data["access_token"]

    response_for_creating_ticket = client.post(
        "/ticket",
        json={"title": "First ticket",
            "description": "This is the frist test ticket"},
        headers={"Authorization": f"Bearer {token}"})

    response_for_creating_ticket_data = response_for_creating_ticket.json()
    create_ticket_owner_id = response_for_creating_ticket_data["owner_id"]


    response_for_list_tickets = client.get(
        "/ticket",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response_for_list_tickets.status_code == 200
    response_for_list_tickets_data = response_for_list_tickets.json()
    assert len(response_for_list_tickets_data) == 1
    assert response_for_list_tickets_data[0]["owner_id"] == create_ticket_owner_id



def test_single_ticket(client):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234"}
    )

    response_for_token = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234"}
    )

    response_for_token_data = response_for_token.json()
    token = response_for_token_data["access_token"]

    response_for_create_ticket = client.post(
        "/ticket",
        json={"title": "First Ticket",
              "description": "This is the frist ticket"},
        headers={"Authorization": f"Bearer {token}"})

    response_for_create_ticket_data = response_for_create_ticket.json()
    create_ticket_id = response_for_create_ticket_data["id"]
    create_ticket_owner_id = response_for_create_ticket_data["owner_id"]

    response_for_get_single_ticket = client.get(
        f"/ticket/{create_ticket_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response_for_get_single_ticket.status_code == 200
    response_for_get_single_ticket_data = response_for_get_single_ticket.json()
    assert response_for_get_single_ticket_data["owner_id"] == create_ticket_owner_id





















