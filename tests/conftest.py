import pytest
import requests
from unittest.mock import patch

@pytest.fixture(autouse=True)
def prevent_real_api_calls():
    """Prevents any real API requests by mocking requests globally."""
    with patch("requests.post") as mock_post, \
         patch("requests.get") as mock_get, \
         patch("requests.delete") as mock_delete:

        # Default mocks return a generic successful response
        mock_post.return_value = requests.Response()
        mock_post.return_value.status_code = 200
        mock_post.return_value._content = b'{"status": "mocked_success"}'

        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value._content = b'{"status": "mocked_success"}'

        mock_delete.return_value = requests.Response()
        mock_delete.return_value.status_code = 200
        mock_delete.return_value._content = b'{"status": "mocked_success"}'

        yield
