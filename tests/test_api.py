from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_get_all_posts_end_point():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.get("/post/")
        assert response.status_code == 200


@patch("app.users.crud.send_message.delay")
@pytest.mark.asyncio
async def test_create_user_end_point(mock_delay):
    mock_delay.return_value = None
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/user/registration/", json={
            "username": "Weit",
            "password": "123456",
            "email": "kloader145@gmail.com"
        })
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_all_users_end_point():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.delete("/user/admin/")
        assert response.status_code == 204
