from app.models import User, UserRole
from app.auth import get_hashed_password




# Tests that a logged-in user can successfully create a new ticket (POST /ticket)
from conftest import engine


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

# Tests that requesting a ticket_id that doesn't exist returns 404
def test_non_existing_ticket(client):
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


    response_for_get_single_non_existing_ticket = client.get(
        f"/ticket/{999999999}",
        headers={"Authorization": f"Bearer {token}"})

    assert response_for_get_single_non_existing_ticket.status_code == 404

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

# Tests that a user who is NOT the ticket owner gets 403 when trying to PATCH (update) that ticket

def test_patch_ticket_forbidden_for_other_user(client):

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

    response_for_patch_single_ticket = client.patch(
        f"/ticket/{create_ticket_id}",
        json={"title": "Updated ticket", "description": "This is the updated ticket"},
        headers={"Authorization": f"Bearer {token_1}"}
    )

    assert response_for_patch_single_ticket.status_code == 403

# Tests that the ticket owner (regular user) gets 403 when trying to update status/resolution on their own ticket

def test_owner_cannot_update_status_or_resolution(client):
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
            json={"status": "SOLVED", "resolution": "The ticket was resolved"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response_for_ticket_update.status_code == 403

# Tests that a user can successfully delete their own ticket (DELETE /ticket/{ticket_id})

def test_for_deleting_own_ticket(client):
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

    response_for_ticket_data = response_for_create_ticket.json()
    create_ticket_id = response_for_ticket_data["id"]

    response_for_deletion = client.delete(
        f"/ticket/{create_ticket_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response_for_deletion.status_code == 204

    response_for_get_single_ticket = client.get(
        f"/ticket/{create_ticket_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response_for_get_single_ticket.status_code == 404

# Tests that a user who is NOT the ticket owner gets 403 when trying to DELETE that ticket
def test_deletion_forbidden_for_other_users(client):
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

    response_for_deletion = client.delete(
        f"/ticket/{create_ticket_id}",
        headers={"Authorization": f"Bearer {token_1}"}
    )

    assert response_for_deletion.status_code == 403

# Tests that an admin can see ALL tickets (not just their own) via GET /ticket
def test_admin_can_see_all_tickets(client, session):
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

    client.post(
        "/ticket",
        json={"title": "First test",
              "description": "This is the first test",
              },
        headers={"Authorization": f"Bearer {token}"}
    )

    admin = User(
        username = "Admin1",
        role = UserRole.admin,
        hashed_password = get_hashed_password("1234")
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    response_for_admin_token = client.post(
        "/token",
        data={"username": "Admin1", "password": "1234"}
    )

    response_for_admin_token_data = response_for_admin_token.json()
    admin_token = response_for_admin_token_data["access_token"]

    response_for_get_all_tickets = client.get(
        "/ticket",

        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response_for_get_all_tickets.status_code == 200
    data = response_for_get_all_tickets.json()
    assert len(data) == 1


# Tests that an admin can update status/resolution on a ticket they don't own (PATCH /ticket/{ticket_id})
def test_admin_can_update_status_and_resolution(client, session):
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

    response_for_ticket = client.post(
        "/ticket",
        json={"title": "First test",
              "description": "This is the first test",
              },
        headers={"Authorization": f"Bearer {token}"}
    )

    response_for_ticket_data = response_for_ticket.json()
    ticket_id = response_for_ticket_data["id"]

    admin = User(
        username="Admin1",
        role=UserRole.admin,
        hashed_password=get_hashed_password("1234")
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    response_for_admin_token = client.post(
        "/token",
        data={"username": "Admin1", "password": "1234"}
    )

    response_for_admin_token_data = response_for_admin_token.json()
    admin_token = response_for_admin_token_data["access_token"]

    response_for_admin_ticket_update = client.patch(
        f"/ticket/{ticket_id}",
        json = {"resolution": "This was approved", "status": "SOLVED"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response_for_admin_ticket_update.status_code == 200
    response_for_admin_ticket_update_data = response_for_admin_ticket_update.json()
    assert response_for_admin_ticket_update_data["resolution"] == "This was approved"
    assert response_for_admin_ticket_update_data["status"] == "SOLVED"


def test_admin_can_see_single_ticket(client, session):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234"}
    )

    response_for_client_token = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234"}
    )

    response_for_client_token_data = response_for_client_token.json()
    client_token = response_for_client_token_data["access_token"]


    response_for_create_ticket = client.post(
        "/ticket",
        json={"title": "First Ticket", "description": "This is the first test ticket"},

        headers={"Authorization": f"Bearer {client_token}"}
    )


    response_for_create_ticket_data = response_for_create_ticket.json()
    ticket_id = response_for_create_ticket_data["id"]

    admin = User(
        username="Admin1",
        role= UserRole.admin,
        hashed_password = get_hashed_password("1234")
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    response_for_admin_token = client.post(
        "/token",
        data={"username": "Admin1", "password": "1234"}
    )

    response_for_admin_token_data = response_for_admin_token.json()
    admin_token = response_for_admin_token_data["access_token"]


    response_for_get_single_ticket_admin = client.get(
        f"/ticket/{ticket_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response_for_get_single_ticket_admin.status_code == 200
    data = response_for_get_single_ticket_admin.json()
    assert data["id"] == ticket_id


def test_admin_can_delete_any_ticket(client, session):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234"}
    )

    response_for_client_token = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234"}
    )

    response_for_client_token_data = response_for_client_token.json()
    client_token = response_for_client_token_data["access_token"]

    response_for_create_ticket = client.post(
        "/ticket",
        json={"title": "First Ticket", "description": "This is the first test ticket"},

        headers={"Authorization": f"Bearer {client_token}"}
    )

    response_for_create_ticket_data = response_for_create_ticket.json()
    ticket_id = response_for_create_ticket_data["id"]

    admin = User(
        username="Admin1",
        role=UserRole.admin,
        hashed_password=get_hashed_password("1234")
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    response_for_admin_token = client.post(
        "/token",
        data={"username": "Admin1", "password": "1234"}
    )

    response_for_admin_token_data = response_for_admin_token.json()
    admin_token = response_for_admin_token_data["access_token"]

    response_for_delete_ticket = client.delete(
        f"/ticket/{ticket_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response_for_delete_ticket.status_code == 204

    response_for_getting_deleted_ticket = client.delete(
        f"/ticket/{ticket_id}",
        headers={"Authorization": f"Bearer {admin_token}"})

    assert response_for_getting_deleted_ticket.status_code == 404









