# Tests that a logged-in user can successfully create a new ticket (POST /ticket)
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


# Tests that GET /ticket returns only the tickets owned by the logged-in user
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


# Tests that GET /ticket/{ticket_id} returns the correct single ticket for its owner
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


# Tests that a user who is NOT the ticket owner gets 403 when trying to GET that ticket
def test_get_ticket_forbidden_for_other_user(client):

    client.post(
        "/register",
        json={"username": "Bogdan1", "password": "12345"}
    )

    response_for_token_1 = client.post(
        "/token",
        data={"username": "Bogdan1", "password": "12345"}
    )

    response_for_token_data_1 = response_for_token_1.json()
    token_1 = response_for_token_data_1["access_token"]



    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234"}
    )

    response_for_token_2 = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234"}
    )

    response_for_token_data_2 = response_for_token_2.json()
    token_2 = response_for_token_data_2["access_token"]

    response_for_create_ticket = client.post(
        "/ticket",
        json={"title": "First Ticket",
              "description": "This is the frist ticket"},
        headers={"Authorization": f"Bearer {token_2}"})

    response_for_create_ticket_data = response_for_create_ticket.json()
    create_ticket_id = response_for_create_ticket_data["id"]

    response_for_get_single_ticket = client.get(
        f"/ticket/{create_ticket_id}",
        headers={"Authorization": f"Bearer {token_1}"}
    )

    assert response_for_get_single_ticket.status_code == 403


# Tests that a user can successfully update their own ticket's title/description (PATCH /ticket/{ticket_id})
def test_update_own_ticket(client):
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
        json={"title": "First test",
              "description": "This is the first test",
              },
        headers={"Authorization": f"Bearer {token}"}
    )

    response_for_create_ticket_data = response_for_create_ticket.json()
    create_ticket_id = response_for_create_ticket_data["id"]

    response_for_ticket_update = client.patch(
        f"/ticket/{create_ticket_id}",
        json={"title": "Updated ticket", "description": "This is the updated ticket"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response_for_ticket_update.status_code == 200
    data = response_for_ticket_update.json()
    assert data["title"] == "Updated ticket"
    assert data["description"] == "This is the updated ticket"



