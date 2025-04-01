# /backend/auth/tests/test_cookies.py
# Unit tests for cookie-setting utility used during login/logout/token refresh

import pytest
from fastapi import Response
from backend.auth.utils.cookies import set_auth_cookies
from backend.core.settings import settings


def test_set_auth_cookies_dev_environment(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    response = Response()
    set_auth_cookies(response, "access123", "refresh123")

    cookies = response.headers.getlist("set-cookie")
    assert any("access_token=access123" in c for c in cookies)
    assert any("refresh_token=refresh123" in c for c in cookies)
    assert any("has_session=1" in c for c in cookies)
    assert all("Secure" not in c for c in cookies)  # Not secure in dev
    assert all("SameSite=Lax" in c for c in cookies if "has_session" not in c)


def test_set_auth_cookies_prod_environment(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    response = Response()
    set_auth_cookies(response, "prod_access", "prod_refresh")

    cookies = response.headers.getlist("set-cookie")
    assert any(
        "access_token=prod_access" in c and "Secure" in c and "SameSite=None" in c
        for c in cookies
    )
    assert any(
        "refresh_token=prod_refresh" in c and "Secure" in c and "SameSite=None" in c
        for c in cookies
    )
