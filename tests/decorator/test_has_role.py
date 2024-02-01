import asyncio
import unittest
from unittest.mock import patch, AsyncMock
from uuid import uuid4

from fastapi import Request, HTTPException

from app.clients.schemas.user_schemas import UserResponse
from app.decorator.has_role import has_role


class TestHasRole(unittest.TestCase):

    @patch("app.decorator.has_role.oauth2_scheme.__call__", new_callable=AsyncMock)
    @patch("app.clients.user_service_client.fetch_user_by_token", new_callable=AsyncMock)
    def test_has_role(self, mock_fetch_user_by_token, mock_oauth2_scheme_call):
        test_user_response = UserResponse(
            id=str(uuid4()),
            name="testuser",
            role="admin",
            token="valid_token"
        )
        mock_fetch_user_by_token.return_value = test_user_response
        mock_oauth2_scheme_call.return_value = "valid_token"

        async def async_test():
            request = Request(scope={"type": "http"})

            @has_role(["admin"])
            async def mock_func(request: Request):
                return "Mock Response"

            response = await mock_func(request)
            self.assertEqual(response, "Mock Response")

        asyncio.run(async_test())

    @patch("app.decorator.has_role.oauth2_scheme.__call__", new_callable=AsyncMock)
    @patch("app.clients.user_service_client.fetch_user_by_token", new_callable=AsyncMock)
    def test_has_role_missing_token(self, mock_fetch_user_by_token, mock_oauth2_scheme_call):
        test_user_response = UserResponse(
            id=str(uuid4()),
            name="testuser",
            role="editor",
            token="valid_token"
        )
        mock_fetch_user_by_token.return_value = test_user_response
        mock_oauth2_scheme_call.return_value = None

        async def async_test():
            request = Request(scope={"type": "http"})

            @has_role(["admin"])
            async def mock_func(request: Request):
                return "Mock Response"

            try:
                await mock_func(request)
            except HTTPException as exc:
                return exc
            return None

        exception = asyncio.run(async_test())

        self.assertEqual(401, exception.status_code)
        self.assertEqual("Unauthorized", exception.detail)

    @patch("app.decorator.has_role.oauth2_scheme.__call__", new_callable=AsyncMock)
    @patch("app.clients.user_service_client.fetch_user_by_token", new_callable=AsyncMock)
    def test_has_role_user_not_found(self, mock_fetch_user_by_token, mock_oauth2_scheme_call):

        mock_fetch_user_by_token.return_value = None
        mock_oauth2_scheme_call.return_value = "invalid_token"

        async def async_test():
            request = Request(scope={"type": "http"})

            @has_role(["admin"])
            async def mock_func(request: Request):
                return "Mock Response"

            try:
                await mock_func(request)
            except HTTPException as exc:
                return exc
            return None

        exception = asyncio.run(async_test())
        self.assertEqual(404, exception.status_code)
        self.assertEqual(f"User with token invalid_token not found", exception.detail)
        mock_fetch_user_by_token.assert_called_once_with("invalid_token")

    @patch("app.decorator.has_role.oauth2_scheme.__call__", new_callable=AsyncMock)
    @patch("app.clients.user_service_client.fetch_user_by_token", new_callable=AsyncMock)
    def test_has_role_inappropriate_role(self, mock_fetch_user_by_token, mock_oauth2_scheme_call):
        test_user_response = UserResponse(
            id=str(uuid4()),
            name="testuser",
            role="editor",
            token="valid_token"
        )
        mock_fetch_user_by_token.return_value = test_user_response
        mock_oauth2_scheme_call.return_value = "valid_token"

        async def async_test():
            request = Request(scope={"type": "http"})

            @has_role(["admin"])
            async def mock_func(request: Request):
                return "Mock Response"

            try:
                await mock_func(request)
            except HTTPException as exc:
                return exc
            return None

        exception = asyncio.run(async_test())

        self.assertEqual(403, exception.status_code)
        self.assertEqual("Forbidden", exception.detail)
        mock_fetch_user_by_token.assert_called_once_with("valid_token")
