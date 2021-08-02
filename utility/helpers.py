import datetime
import jwt
import json
import requests
from django.conf import settings


def gettoken(email, password):
    '''
    :param email:
    :param password:
    :return: access and refresh token
    '''
    payload = {
        'email': email,
        'password': password,
    }
    url = settings.TOKEN_URL
    url_response = requests.post(url, payload)
    response = json.loads(url_response.text)

    return response


def decode_jwt_token(request):
    token = request.headers['Authorization'].split(' ')[1]
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    return decoded_token


def validate_decoded_token(request, queryObject):
    decodedToken = decode_jwt_token(request)
    user_id = decodedToken['user_id']
    if queryObject.author_id.id != user_id:
        return False

    return True


def set_token_expiry():
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    return str(expiry)


def set_token_iat():
    iat = datetime.datetime.utcnow()
    return str(iat)
