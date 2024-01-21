"""Contains unittests for todo application."""
from collections import Counter

from flask.testing import FlaskClient


def test_get_all_todos(client: FlaskClient, auth_headers):
    """Test that the list of todos is empty."""
    # GIVEN the list of todos is empty
    # WHEN the user requests the list of todos
    response = client.get("/todos", headers=auth_headers)
    # THEN the status code should be 200
    assert response.status_code == 200
    # AND the list of todos is empty
    assert response.get_json()["items"] == []


def test_add_todo(client: FlaskClient, auth_headers):
    """Test adding a new todo item."""
    # GIVEN the list of todo items is empty
    # WHEN the user adds a new todo item
    data = {"task": "New Task"}
    response = client.post("/todos", json=data, headers=auth_headers)
    # THEN the response status code is 201
    assert response.status_code == 201
    # AND the response should equal the new todo with id 1
    filtered_dict = _create_filtered_dict(response.get_json())
    assert Counter(filtered_dict) == Counter({"id": 1, "task": "New Task"})


def test_get_todo(client: FlaskClient, auth_headers):
    """Test retrieving an existing todo item."""
    # GIVEN there is only one todo item with id 1
    client.post("/todos", json={"task": "New Task"}, headers=auth_headers)
    # WHEN the user requests todo item with id 1
    response = client.get("/todos/1", headers=auth_headers)
    # THEN the response status code should be 200
    assert response.status_code == 200
    # AND the response content should contain the task with id 1
    filtered_dict = _create_filtered_dict(response.get_json())
    assert Counter(filtered_dict) == Counter({"id": 1, "task": "New Task"})


def test_update_todo(client: FlaskClient, auth_headers):
    """Test updating an existing todo item."""
    # GIVEN there is only one todo item with id 1
    client.post("/todos", json={"task": "Original Task"}, headers=auth_headers)
    # WHEN the user updates the todo item with id 1
    response = client.put(
        "/todos/1", json={"task": "Updated Task"}, headers=auth_headers
    )
    # THEN the response status code should be 200
    assert response.status_code == 200
    # AND the response should contain the updated todo item with id 1
    filtered_dict = _create_filtered_dict(response.get_json())
    assert Counter(filtered_dict) == Counter({"id": 1, "task": "Updated Task"})


def test_delete_todo(client: FlaskClient, auth_headers):
    """Test deleting an existing todo item."""
    # GIVEN there is only one todo item with id 1
    client.post("/todos", json={"task": "To be deleted"}, headers=auth_headers)
    # WHEN the user requests to delete the todo item with id 1
    response = client.delete("/todos/1", headers=auth_headers)
    # THEN the response status code should be 200
    assert response.status_code == 204


def test_delete_nonexistent_todo(client: FlaskClient, auth_headers):
    """Test deleting a nonexisting todo item."""
    # GIVEN there is not todo item with id 1
    # WHEN the user requests to delete the todo item with id 1
    response = client.delete("/todos/1", headers=auth_headers)
    # THEN the response status code should be 404
    assert response.status_code == 404
    # AND the response should contain an error message indicating
    # that the item with id 1 does not exist
    expected_message = {
        "message": "The requested URL was not found on the server. "
        "If you entered the URL manually please check your spelling and "
        "try again. "
        "You have requested this URI [/todos/1] but did you mean "
        "/todos/<int:todo_id> or /todos ?"
    }
    assert response.get_json() == expected_message


def _create_filtered_dict(response: dict) -> dict:
    """Create a new dictionary with only the specified keys."""
    selected_keys = {"id", "task"}  # Use a set for faster membership tests
    return {key: response[key] for key in selected_keys.intersection(response)}
