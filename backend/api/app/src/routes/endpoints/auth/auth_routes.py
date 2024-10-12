from quart import Blueprint, jsonify, request, current_app
from app.src.errors.api import APIError
import jwt
import datetime
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
async def login():
    data = await request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise APIError("Missing email or password", status_code=400)

    query = """
    SELECT au.id, au.password_hash, a.email
    FROM account_user au
    JOIN account a ON au.account_id = a.id
    WHERE a.email = $1
    """

    user = await current_app.pg_db.fetchrow(query, email)

    if not user:
        raise APIError("Invalid email or password", status_code=401)

    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        raise APIError("Invalid email or password", status_code=401)

    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow() 
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})

@auth_bp.route('/logout', methods=['POST'])
async def logout():
    return jsonify({"message": "Successfully logged out"}), 200