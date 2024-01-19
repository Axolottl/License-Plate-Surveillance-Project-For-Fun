from jose import jwt
from datetime import datetime, timedelta
from settings import SECRET_KEY

def generate_access_token(username):
    """
    Generate an access token for the given username.
    """
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        'sub': username,
        'exp': expiration_time,
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
