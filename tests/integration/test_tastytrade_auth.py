import pytest
from jedgebot.broker.tastytrade_broker import TastyTradeBroker

@pytest.fixture
def broker():
    return TastyTradeBroker()

def test_authentication(broker):
    """Test that authentication retrieves a session token."""
    assert broker.token is not None, "Authentication failed, token is None"
