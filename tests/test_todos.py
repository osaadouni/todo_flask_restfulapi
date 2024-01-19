"""Contains unittests for todo application."""


def test_get_all_todos(client):
    """Test that the list of todos is empty.

    :type client: object
    """
    # GIVEN the list of todos is empty
    # WHEN the user requests the list of todos
    response = client.get('/todos')
    # THEN the status code should be 200
    assert response.status_code == 200
    # AND the list of todos is empty
    assert response.get_json() == []


def test_add_todo(client):
    """Test adding a new todo item.

    :type client: object
    """
    # GIVEN the list of todo items is empty
    # WHEN the user adds a new todo item
    response = client.post('/todos', json={'task': 'New Task'})
    # THEN the response status code is 201
    assert response.status_code == 201
    # AND the response should equal the new todo with id 1
    assert response.get_json() == {'task': 'New Task', 'id': 1}


def test_get_todo(client):
    """Test retrieving an existing todo item.

    :type client: object
    """
    # GIVEN there is only one todo item with id 1
    client.post('/todos', json={'task': 'Test Task'})
    # WHEN the user requests todo item with id 1
    response = client.get('/todos/1')
    # THEN the response status code should be 200
    assert response.status_code == 200
    # AND the response content should contain the task with id 1
    assert response.get_json() == {'task': 'Test Task', 'id': 1}


def test_update_todo(client):
    """Test updating an existing todo item.

    :type client: object
    """
    # GIVEN there is only one todo item with id 1
    client.post('/todos', json={'task': 'Original Task'})
    # WHEN the user updates the todo item with id 1
    response = client.put('/todos/1', json={'task': 'Updated Task'})
    # THEN the response status code should be 200
    assert response.status_code == 200
    # AND the response should contain the updated todo item with id 1
    assert response.get_json() == {'id': 1, 'task': 'Updated Task'}


def test_delete_todo(client):
    """Test deleting an existing todo item.

    :type client: object
    """
    # GIVEN there is only one todo item with id 1
    client.post('/todos', json={'task': 'To be deleted'})
    # WHEN the user requests to delete the todo item with id 1
    response = client.delete('/todos/1')
    # THEN the response status code should be 200
    assert response.status_code == 204


def test_delete_nonexistent_todo(client):
    """Test deleting a nonexisting todo item.

    :type client: object
    """
    # GIVEN there is not todo item with id 1
    # WHEN the user requests to delete the todo item with id 1
    response = client.delete('/todos/1')
    # THEN the response status code should be 404
    assert response.status_code == 404
    # AND the response should contain an error message indicating
    # that the item with id 1 does not exist
    expected_message = {
        'message': "The requested URL was not found on the server. "
                   "If you entered the URL manually please check your spelling and try again. "
                   "You have requested this URI [/todos/1] but did you mean /todos/<int:todo_id> or /todos ?"}
    assert response.get_json() == expected_message
