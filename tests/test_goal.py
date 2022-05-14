import json

from run import app

def test_add_goal():
    client = app.test_client()
    url = '/add-goal'

    mock_request_data = {
        "id": "10",
        "user_id": "1",
        "label": "sfd",
        "description": "description",
        "done": "false",
        "summary": "summary"
    }

    response = client.post(url, data=json.dumps(mock_request_data))
    assert response.status_code == 200


def test_show_goal():
    client = app.test_client()
    url = '/get-goals'

    mock_request_data = {
        "user_id": "1",
    }

    response = client.post(url, data=json.dumps(mock_request_data))
    assert response.status_code == 200


def test_change_goal():
    client = app.test_client()
    url = '/edit-goal'

    mock_request_data = {
        "id": "10",
        "user_id": "1",
        "label": "sfd",
        "description": "asdfasd",
        "done": "false",
        "summary": "summary"
    }

    response = client.post(url, data=json.dumps(mock_request_data))
    assert response.status_code == 200


def test_remove_goal():
    client = app.test_client()
    url = '/remove-goal'

    mock_request_data = {
        "id": "10",
    }

    response = client.post(url, data=json.dumps(mock_request_data))
    assert response.status_code == 200

