from quart import Blueprint, jsonify, request, current_app
from app.src.errors.api import APIError
from app.src.utils.auth import token_required
import bcrypt
from datetime import datetime

user_account_bp = Blueprint('user_account', __name__)

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper function to convert to integer
def to_int(value, field_name):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise APIError(f"{field_name} must be an integer", status_code=400)

# Helper function to convert to integer or return None
def to_int_or_none(value, field_name):
    if value is None or value == '':
        return None
    try:
        return int(value)
    except ValueError:
        raise APIError(f"{field_name} must be an integer", status_code=400)

# Account User CRUD

@user_account_bp.route('/account_user', methods=['POST'])
@token_required
async def create_account_user(current_user):
    try:
        data = await request.json
        required_fields = ['account_id', 'password', 'role']
        if not all(field in data for field in required_fields):
            raise APIError("Missing required fields", status_code=400)
        
        password_hash = hash_password(data['password'])
        
        query = """
        INSERT INTO account_user (account_id, password_hash, role)
        VALUES ($1, $2, $3)
        RETURNING id
        """
        user_id = await current_app.pg_db.fetchval(query, 
                                                   to_int(data['account_id'], 'account_id'), 
                                                   password_hash, 
                                                   to_int(data['role'], 'role'))
        return jsonify({'message': 'Account user created successfully', 'id': user_id}), 201
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error creating account user: {str(e)}", status_code=500)

@user_account_bp.route('/account_user', methods=['GET'])
@token_required
async def get_all_account_users(current_user):
    try:
        users = await current_app.pg_db.fetch("SELECT * FROM account_user")
        return jsonify([dict(row) for row in users])
    except Exception as e:
        raise APIError(f"Error fetching account users: {str(e)}", status_code=500)

@user_account_bp.route('/account_user/<int:user_id>', methods=['GET'])
@token_required
async def get_account_user(current_user, user_id):
    try:
        user = await current_app.pg_db.fetchrow("SELECT * FROM account_user WHERE id = $1", user_id)
        if user is None:
            raise APIError("Account user not found", status_code=404)
        return jsonify(dict(user))
    except Exception as e:
        raise APIError(f"Error fetching account user: {str(e)}", status_code=500)

@user_account_bp.route('/account_user/<int:user_id>', methods=['PUT'])
@token_required
async def update_account_user(current_user, user_id):
    try:
        data = await request.json
        query = """
        UPDATE account_user
        SET account_id = COALESCE($1, account_id),
            password_hash = COALESCE($2, password_hash),
            role = COALESCE($3, role),
            modified = $4
        WHERE id = $5
        """
        password_hash = hash_password(data['password']) if 'password' in data else None
        await current_app.pg_db.execute(
            query,
            to_int(data.get('account_id'), 'account_id') if 'account_id' in data else None,
            password_hash,
            to_int(data.get('role'), 'role') if 'role' in data else None,
            datetime.now(),
            user_id
        )
        return jsonify({'message': 'Account user updated successfully'})
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error updating account user: {str(e)}", status_code=500)

@user_account_bp.route('/account_user/<int:user_id>', methods=['DELETE'])
@token_required
async def delete_account_user(current_user, user_id):
    try:
        result = await current_app.pg_db.execute("DELETE FROM account_user WHERE id = $1", user_id)
        if result == "DELETE 1":
            return jsonify({'message': 'Account user deleted successfully'})
        else:
            raise APIError("Account user not found", status_code=404)
    except Exception as e:
        raise APIError(f"Error deleting account user: {str(e)}", status_code=500)

# Account User Role CRUD

@user_account_bp.route('/account_user_role', methods=['POST'])
@token_required
async def create_account_user_role(current_user):
    try:
        data = await request.json
        required_fields = ['slug', 'name']
        if not all(field in data for field in required_fields):
            raise APIError("Missing required fields", status_code=400)
        
        query = """
        INSERT INTO account_user_role (slug, name)
        VALUES ($1, $2)
        RETURNING id
        """
        role_id = await current_app.pg_db.fetchval(query, data['slug'], data['name'])
        return jsonify({'message': 'Account user role created successfully', 'id': role_id}), 201
    except Exception as e:
        raise APIError(f"Error creating account user role: {str(e)}", status_code=500)

@user_account_bp.route('/account_user_role', methods=['GET'])
@token_required
async def get_all_account_user_roles(current_user):
    try:
        roles = await current_app.pg_db.fetch("SELECT * FROM account_user_role")
        return jsonify([dict(row) for row in roles])
    except Exception as e:
        raise APIError(f"Error fetching account user roles: {str(e)}", status_code=500)

@user_account_bp.route('/account_user_role/<int:role_id>', methods=['GET'])
@token_required
async def get_account_user_role(current_user, role_id):
    try:
        role = await current_app.pg_db.fetchrow("SELECT * FROM account_user_role WHERE id = $1", role_id)
        if role is None:
            raise APIError("Account user role not found", status_code=404)
        return jsonify(dict(role))
    except Exception as e:
        raise APIError(f"Error fetching account user role: {str(e)}", status_code=500)

@user_account_bp.route('/account_user_role/<int:role_id>', methods=['PUT'])
@token_required
async def update_account_user_role(current_user, role_id):
    try:
        data = await request.json
        query = """
        UPDATE account_user_role
        SET slug = COALESCE($1, slug),
            name = COALESCE($2, name),
            modified = $3
        WHERE id = $4
        """
        await current_app.pg_db.execute(
            query,
            data.get('slug'),
            data.get('name'),
            datetime.now(),
            role_id
        )
        return jsonify({'message': 'Account user role updated successfully'})
    except Exception as e:
        raise APIError(f"Error updating account user role: {str(e)}", status_code=500)

@user_account_bp.route('/account_user_role/<int:role_id>', methods=['DELETE'])
@token_required
async def delete_account_user_role(current_user, role_id):
    try:
        result = await current_app.pg_db.execute("DELETE FROM account_user_role WHERE id = $1", role_id)
        if result == "DELETE 1":
            return jsonify({'message': 'Account user role deleted successfully'})
        else:
            raise APIError("Account user role not found", status_code=404)
    except Exception as e:
        raise APIError(f"Error deleting account user role: {str(e)}", status_code=500)

# ... (continued from previous part)

# Account CRUD

@user_account_bp.route('/account', methods=['POST'])
@token_required
async def create_account(current_user):
    try:
        data = await request.json
        required_fields = ['first_name', 'last_name', 'email']
        if not all(field in data for field in required_fields):
            raise APIError("Missing required fields", status_code=400)
        
        query = """
        INSERT INTO account (first_name, last_name, business_name, business_abn, phone, email, account_address_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
        """
        account_id = await current_app.pg_db.fetchval(
            query,
            data['first_name'],
            data['last_name'],
            data.get('business_name'),
            to_int_or_none(data.get('business_abn'), 'business_abn'),
            data.get('phone'),
            data['email'],
            to_int_or_none(data.get('account_address_id'), 'account_address_id')
        )
        return jsonify({'message': 'Account created successfully', 'id': account_id}), 201
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error creating account: {str(e)}", status_code=500)

@user_account_bp.route('/account', methods=['GET'])
@token_required
async def get_all_accounts(current_user):
    try:
        accounts = await current_app.pg_db.fetch("SELECT * FROM account")
        return jsonify([dict(row) for row in accounts])
    except Exception as e:
        raise APIError(f"Error fetching accounts: {str(e)}", status_code=500)

@user_account_bp.route('/account/<int:account_id>', methods=['GET'])
@token_required
async def get_account(current_user, account_id):
    try:
        account = await current_app.pg_db.fetchrow("SELECT * FROM account WHERE id = $1", account_id)
        if account is None:
            raise APIError("Account not found", status_code=404)
        return jsonify(dict(account))
    except Exception as e:
        raise APIError(f"Error fetching account: {str(e)}", status_code=500)

@user_account_bp.route('/account/<int:account_id>', methods=['PUT'])
@token_required
async def update_account(current_user, account_id):
    try:
        data = await request.json
        query = """
        UPDATE account
        SET first_name = COALESCE($1, first_name),
            last_name = COALESCE($2, last_name),
            business_name = $3,
            business_abn = $4,
            phone = COALESCE($5, phone),
            email = COALESCE($6, email),
            account_address_id = $7
        WHERE id = $8
        """
        await current_app.pg_db.execute(
            query,
            data.get('first_name'),
            data.get('last_name'),
            data.get('business_name'),
            to_int_or_none(data.get('business_abn'), 'business_abn'),
            data.get('phone'),
            data.get('email'),
            to_int_or_none(data.get('account_address_id'), 'account_address_id'),
            account_id
        )
        return jsonify({'message': 'Account updated successfully'})
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error updating account: {str(e)}", status_code=500)

@user_account_bp.route('/account/<int:account_id>', methods=['DELETE'])
@token_required
async def delete_account(current_user, account_id):
    try:
        result = await current_app.pg_db.execute("DELETE FROM account WHERE id = $1", account_id)
        if result == "DELETE 1":
            return jsonify({'message': 'Account deleted successfully'})
        else:
            raise APIError("Account not found", status_code=404)
    except Exception as e:
        raise APIError(f"Error deleting account: {str(e)}", status_code=500)

# Account Address CRUD

@user_account_bp.route('/account_address', methods=['POST'])
@token_required
async def create_account_address(current_user):
    try:
        data = await request.json
        required_fields = ['street', 'suburb_city', 'postcode', 'state_id']
        if not all(field in data for field in required_fields):
            raise APIError("Missing required fields", status_code=400)
        
        query = """
        INSERT INTO account_address (unit, street, suburb_city, postcode, state_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        address_id = await current_app.pg_db.fetchval(
            query,
            data.get('unit'),
            data['street'],
            data['suburb_city'],
            to_int(data['postcode'], 'postcode'),
            to_int(data['state_id'], 'state_id')
        )
        return jsonify({'message': 'Account address created successfully', 'id': address_id}), 201
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error creating account address: {str(e)}", status_code=500)

@user_account_bp.route('/account_address', methods=['GET'])
@token_required
async def get_all_account_addresses(current_user):
    try:
        addresses = await current_app.pg_db.fetch("SELECT * FROM account_address")
        return jsonify([dict(row) for row in addresses])
    except Exception as e:
        raise APIError(f"Error fetching account addresses: {str(e)}", status_code=500)

@user_account_bp.route('/account_address/<int:address_id>', methods=['GET'])
@token_required
async def get_account_address(current_user, address_id):
    try:
        address = await current_app.pg_db.fetchrow("SELECT * FROM account_address WHERE id = $1", address_id)
        if address is None:
            raise APIError("Account address not found", status_code=404)
        return jsonify(dict(address))
    except Exception as e:
        raise APIError(f"Error fetching account address: {str(e)}", status_code=500)

@user_account_bp.route('/account_address/<int:address_id>', methods=['PUT'])
@token_required
async def update_account_address(current_user, address_id):
    try:
        data = await request.json
        query = """
        UPDATE account_address
        SET unit = COALESCE($1, unit),
            street = COALESCE($2, street),
            suburb_city = COALESCE($3, suburb_city),
            postcode = COALESCE($4, postcode),
            state_id = COALESCE($5, state_id),
            modified = $6
        WHERE id = $7
        """
        await current_app.pg_db.execute(
            query,
            data.get('unit'),
            data.get('street'),
            data.get('suburb_city'),
            to_int(data.get('postcode'), 'postcode') if 'postcode' in data else None,
            to_int(data.get('state_id'), 'state_id') if 'state_id' in data else None,
            datetime.now(),
            address_id
        )
        return jsonify({'message': 'Account address updated successfully'})
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error updating account address: {str(e)}", status_code=500)

@user_account_bp.route('/account_address/<int:address_id>', methods=['DELETE'])
@token_required
async def delete_account_address(current_user, address_id):
    try:
        result = await current_app.pg_db.execute("DELETE FROM account_address WHERE id = $1", address_id)
        if result == "DELETE 1":
            return jsonify({'message': 'Account address deleted successfully'})
        else:
            raise APIError("Account address not found", status_code=404)
    except Exception as e:
        raise APIError(f"Error deleting account address: {str(e)}", status_code=500)

# Account Address AU State CRUD

@user_account_bp.route('/account_address_au_state', methods=['POST'])
@token_required
async def create_account_address_au_state(current_user):
    try:
        data = await request.json
        required_fields = ['name', 'country_id']
        if not all(field in data for field in required_fields):
            raise APIError("Missing required fields", status_code=400)
        
        query = """
        INSERT INTO account_address_au_state (name, country_id)
        VALUES ($1, $2)
        RETURNING id
        """
        state_id = await current_app.pg_db.fetchval(query, data['name'], to_int(data['country_id'], 'country_id'))
        return jsonify({'message': 'Account address AU state created successfully', 'id': state_id}), 201
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error creating account address AU state: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_au_state', methods=['GET'])
@token_required
async def get_all_account_address_au_states(current_user):
    try:
        states = await current_app.pg_db.fetch("SELECT * FROM account_address_au_state")
        return jsonify([dict(row) for row in states])
    except Exception as e:
        raise APIError(f"Error fetching account address AU states: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_au_state/<int:state_id>', methods=['GET'])
@token_required
async def get_account_address_au_state(current_user, state_id):
    try:
        state = await current_app.pg_db.fetchrow("SELECT * FROM account_address_au_state WHERE id = $1", state_id)
        if state is None:
            raise APIError("Account address AU state not found", status_code=404)
        return jsonify(dict(state))
    except Exception as e:
        raise APIError(f"Error fetching account address AU state: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_au_state/<int:state_id>', methods=['PUT'])
@token_required
async def update_account_address_au_state(current_user, state_id):
    try:
        data = await request.json
        query = """
        UPDATE account_address_au_state
        SET name = COALESCE($1, name),
            country_id = COALESCE($2, country_id),
            modified = $3
        WHERE id = $4
        """
        await current_app.pg_db.execute(
            query,
            data.get('name'),
            to_int(data.get('country_id'), 'country_id') if 'country_id' in data else None,
            datetime.now(),
            state_id
        )
        return jsonify({'message': 'Account address AU state updated successfully'})
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(f"Error updating account address AU state: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_au_state/<int:state_id>', methods=['DELETE'])
@token_required
async def delete_account_address_au_state(current_user, state_id):
    try:
        result = await current_app.pg_db.execute("DELETE FROM account_address_au_state WHERE id = $1", state_id)
        if result == "DELETE 1":
            return jsonify({'message': 'Account address AU state deleted successfully'})
        else:
            raise APIError("Account address AU state not found", status_code=404)
    except Exception as e:
        raise APIError(f"Error deleting account address AU state: {str(e)}", status_code=500)

# Account Address Country CRUD

@user_account_bp.route('/account_address_country', methods=['POST'])
@token_required
async def create_account_address_country(current_user):
    try:
        data = await request.json
        if 'name' not in data:
            raise APIError("Missing required field: name", status_code=400)
        
        query = """
        INSERT INTO account_address_country (name, active)
        VALUES ($1, $2)
        RETURNING id
        """
        country_id = await current_app.pg_db.fetchval(query, data['name'], data.get('active', True))
        return jsonify({'message': 'Account address country created successfully', 'id': country_id}), 201
    except Exception as e:
        raise APIError(f"Error creating account address country: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_country', methods=['GET'])
@token_required
async def get_all_account_address_countries(current_user):
    try:
        query = """
        SELECT * FROM account_address_country
        ORDER BY active DESC, name ASC
        """
        countries = await current_app.pg_db.fetch(query)
        return jsonify([dict(row) for row in countries])
    except Exception as e:
        raise APIError(f"Error fetching account address countries: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_country/<int:country_id>', methods=['GET'])
@token_required
async def get_account_address_country(current_user, country_id):
    try:
        country = await current_app.pg_db.fetchrow("SELECT * FROM account_address_country WHERE id = $1", country_id)
        if country is None:
            raise APIError("Account address country not found", status_code=404)
        return jsonify(dict(country))
    except Exception as e:
        raise APIError(f"Error fetching account address country: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_country/<int:country_id>', methods=['PUT'])
@token_required
async def update_account_address_country(current_user, country_id):
    try:
        data = await request.json
        query = """
        UPDATE account_address_country
        SET name = COALESCE($1, name),
            active = COALESCE($2, active),
            modified = $3
        WHERE id = $4
        """
        await current_app.pg_db.execute(
            query,
            data.get('name'),
            data.get('active'),
            datetime.now(),
            country_id
        )
        return jsonify({'message': 'Account address country updated successfully'})
    except Exception as e:
        raise APIError(f"Error updating account address country: {str(e)}", status_code=500)

@user_account_bp.route('/account_address_country/<int:country_id>', methods=['DELETE'])
@token_required
async def delete_account_address_country(current_user, country_id):
    try:
        result = await current_app.pg_db.execute("DELETE FROM account_address_country WHERE id = $1", country_id)
        if result == "DELETE 1":
            return jsonify({'message': 'Account address country deleted successfully'})
        else:
            raise APIError("Account address country not found", status_code=404)
    except Exception as e:
        raise APIError(f"Error deleting account address country: {str(e)}", status_code=500)