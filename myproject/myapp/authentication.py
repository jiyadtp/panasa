import jwt, datetime
from rest_framework import exceptions

def create_access_token(id):
    payload = {
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
        'iat': datetime.datetime.utcnow()
    }

    access_token = jwt.encode(payload, 'access_secret', algorithm='HS256')
    return access_token


def decode_access_token(access_token):
    try:
        decoded_token = jwt.decode(access_token, 'access_secret', algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise exceptions.AuthenticationFailed('unauthenticated')
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None
    except:
        return None