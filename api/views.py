import json

from django.shortcuts import render
from django.http import JsonResponse
import jwt
from datetime import datetime, timedelta, timezone

JWT_SECRET = "amjshdgasd467y81ugyhdbsa"

user = None

def secret_view(request):
    if "Authorization" in request.headers:
        print("ok")
        if len(request.headers["Authorization"].split(" ")) == 2:
            print("ok")
            token = request.headers["Authorization"].split(" ")[1]
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], verify=True, options={
                    "verify_signature": True,
                    "verify_exp": "verify_signature",
                    "require": ["exp", "iat"]
                })
                print(payload)
                if payload.get("user_id") == 1:
                    return JsonResponse({"message": "access to superuser"})
                return JsonResponse({"message": "access approved"})
            except Exception as e:
                print(e)

    return JsonResponse({
        "message": "access denied"
    })

def get_tokens():
    access_token = jwt.encode({"user_id": 1, "email": user,"iat":datetime.now(tz=timezone.utc),"exp": datetime.now(tz=timezone.utc) + timedelta(minutes=20)}, JWT_SECRET,
                              algorithm="HS256")
    refresh_token = jwt.encode({"iat":datetime.now(tz=timezone.utc), "exp": datetime.now(tz=timezone.utc) + timedelta(days=30)}, JWT_SECRET, algorithm="HS256")

    return access_token, refresh_token


def get_token_view(request):
    global user

    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    if body_data.get("email") is not None and body_data.get("password") is not None:

        user = body_data.get("email")
        access_token, refresh_token = get_tokens()
        return JsonResponse({
            "access": access_token,
            "refresh": refresh_token
        })
    return JsonResponse({
        "data": {
            "message": "failed get data from body"
        }
    })


def refresh_tokens_view(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    if "Authorization" in request.headers and body_data.get("refresh_token") is not None:
        token = body_data.POST["refresh_token"]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], verify=True, options={
                "verify_signature": True,
                "verify_exp": "verify_signature",
                "require": ["exp", "iat"]
            })
            access_token, refresh_token = get_tokens()
            return JsonResponse({
                "access": access_token,
                "refresh": refresh_token
            })
        except:
            return JsonResponse({
                "data": {
                    "message": "Ошибка декодирования токена"
                }
            })
    return JsonResponse({
        "data": {
            "message": "Validation error",
            "detail": "Missed Authorization or refresh token"
        }
    })

