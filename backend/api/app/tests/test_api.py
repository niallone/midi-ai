import pytest
from quart import Quart

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get('/health')
    assert response.status_code == 200
    data = await response.get_json()
    assert data == {"status": "healthy", "database": "connected"}

# @pytest.mark.asyncio
# async def test_index(client):
#     response = await client.get('/')
#     assert response.status_code == 200
#     data = await response.get_data(as_text=True)
#     assert "Welcome to the API." in data

# class TestAuthRoutes:
#     @pytest.mark.asyncio
#     async def test_login_success(self, client, mock_db, app):
#         app.pg_db = mock_db
#         mock_db.fetchrow.return_value = {"id": 1, "password_hash": "hashed_password", "email": "test@example.com"}
#         response = await client.post('/auth/login', json={"email": "test@example.com", "password": "password123"})
#         assert response.status_code == 200
#         data = await response.get_json()
#         assert "token" in data

#     @pytest.mark.asyncio
#     async def test_login_invalid_credentials(self, client, mock_db, app):
#         app.pg_db = mock_db
#         mock_db.fetchrow.return_value = None
#         response = await client.post('/auth/login', json={"email": "wrong@example.com", "password": "wrongpass"})
#         assert response.status_code == 401

#     @pytest.mark.asyncio
#     async def test_logout(self, client):
#         response = await client.post('/auth/logout')
#         assert response.status_code == 200
#         data = await response.get_json()
#         assert data["message"] == "Successfully logged out"

# class TestAdminRoutes:
#     @pytest.mark.asyncio
#     async def test_protected_admin_route(self, client, admin_token):
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         response = await client.get('/admin/some-protected-route', headers=headers)
#         assert response.status_code == 200

# class TestUserAccountRoutes:
#     @pytest.mark.asyncio
#     async def test_create_account_user(self, client, mock_db, admin_token, app):
#         app.pg_db = mock_db
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         user_data = {"account_id": 1, "password": "newpass123", "role": 2}
#         mock_db.fetchval.return_value = 1
#         response = await client.post('/admin/user/account_user', json=user_data, headers=headers)
#         assert response.status_code == 201
#         data = await response.get_json()
#         assert "id" in data

#     @pytest.mark.asyncio
#     async def test_get_account_users(self, client, mock_db, admin_token, app):
#         app.pg_db = mock_db
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         mock_db.fetch.return_value = [{"id": 1, "account_id": 1, "role": 2}]
#         response = await client.get('/admin/user/account_user', headers=headers)
#         assert response.status_code == 200
#         data = await response.get_json()
#         assert isinstance(data, list)
#         assert len(data) > 0

# class TestChilliRoutes:
#     @pytest.mark.asyncio
#     async def test_get_all_chillis(self, client, mock_db, admin_token):
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         mock_db.fetch.return_value = [{"id": 1, "name": "Jalapeño", "flavours": []}]
#         response = await client.get('/admin/chilli/chilli', headers=headers)
#         assert response.status_code == 200
#         data = await response.get_json()
#         assert isinstance(data, list)
#         assert len(data) > 0

#     @pytest.mark.asyncio
#     async def test_add_chilli(self, client, mock_db, admin_token):
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         chilli_data = {
#             "name": "Habanero",
#             "description": "Very hot chilli",
#             "maturity_category_id": 1,
#             "species_id": 1,
#             "heat_level_id": 1,
#             "filial_id": 1,
#             "parent_1_id": None,
#             "parent_2_id": None,
#             "height_category": 1,
#             "frost_tolerance": 1,
#             "germination_time": 1,
#             "origin_country": 1,
#             "position": 1,
#             "soil": 1,
#             "colour": 1,
#             "lifecycle": 1,
#             "flavours": [1, 2]
#         }
#         mock_db.fetchval.return_value = 1
#         response = await client.post('/admin/chilli/chilli', json=chilli_data, headers=headers)
#         assert response.status_code == 201
#         data = await response.get_json()
#         assert "id" in data

# class TestSeedlingRoutes:
#     @pytest.mark.asyncio
#     async def test_create_seedling(self, client, mock_db, admin_token):
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         seedling_data = {
#             "chilli_id": 1,
#             "status_id": 1,
#             "date_planted": "2023-01-01"
#         }
#         mock_db.fetchval.return_value = 1
#         response = await client.post('/admin/chilli/seedling', json=seedling_data, headers=headers)
#         assert response.status_code == 201
#         data = await response.get_json()
#         assert "id" in data

#     @pytest.mark.asyncio
#     async def test_get_seedlings(self, client, mock_db, admin_token):
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         mock_db.fetch.return_value = [{"id": 1, "chilli_id": 1, "status_id": 1, "date_planted": "2023-01-01"}]
#         response = await client.get('/admin/chilli/seedling', headers=headers)
#         assert response.status_code == 200
#         data = await response.get_json()
#         assert isinstance(data, list)
#         assert len(data) > 0

# class TestSeedlingEventRoutes:
#     @pytest.mark.asyncio
#     async def test_create_seedling_event(self, client, mock_db, admin_token):
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         event_data = {
#             "seedling_id": 1,
#             "event_type_id": 1,
#             "event_date": "2023-01-02",
#             "notes": "First leaves appeared"
#         }
#         mock_db.fetchval.return_value = 1
#         response = await client.post('/admin/chilli/seedling_event', json=event_data, headers=headers)
#         assert response.status_code == 201
#         data = await response.get_json()
#         assert "id" in data

#     @pytest.mark.asyncio
#     async def test_get_seedling_events(self, client, mock_db, admin_token):
#         headers = {'Authorization': f'Bearer {admin_token}'}
#         mock_db.fetch.return_value = [{"id": 1, "seedling_id": 1, "event_type_id": 1, "event_date": "2023-01-02"}]
#         response = await client.get('/admin/chilli/seedling_event', headers=headers)
#         assert response.status_code == 200
#         data = await response.get_json()
#         assert isinstance(data, list)
#         assert len(data) > 0