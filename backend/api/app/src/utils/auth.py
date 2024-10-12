from functools import wraps
from quart import jsonify, request, current_app
import jwt

def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token is malformed'}), 401
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = await current_app.pg_db.fetchrow(
                "SELECT * FROM admin_users WHERE id = $1", data['user_id']
            )
            if current_user is None:
                return jsonify({'message': 'User not found'}), 401
        except Exception as e:
            current_app.logger.error(f"Error in token validation: {str(e)}")
            return jsonify({'message': 'Something went wrong'}), 500
        return await f(current_user, *args, **kwargs)
    return decorated